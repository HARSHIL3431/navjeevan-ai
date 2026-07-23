import uuid
import time
import asyncio
import logging
from backend.models.dtos import (
    AdvisoryRequestDTO, DecisionContextDTO, AdvisoryDTO, AdvisoryMetadataDTO,
    CropStageRequestDTO, CropStageResponseDTO,
    FertilizerRequestDTO, FertilizerResponseDTO,
    IrrigationRequestDTO, IrrigationResponseDTO,
    PestRequestDTO, PestResponseDTO,
    ConfidenceRequestDTO, ConfidenceResponseDTO
)
from backend.decision_engine.providers import WeatherProvider, RuleProvider
from backend.decision_engine.wrapper import ExecutionWrapper

from backend.services import crop_stage_service, fertilizer_service, irrigation_service, pest_service, confidence_service

logger = logging.getLogger(__name__)

class AdvisoryEngine:
    def __init__(self, weather_provider: WeatherProvider, rule_provider: RuleProvider):
        self.weather_provider = weather_provider
        self.rule_provider = rule_provider
        self.penalties = {
            "WEATHER_UNAVAILABLE": -30,
            "MISSING_RAIN_DATA": -20,
            "MISSING_WEATHER_PARAMS": -20,
            "RULE_MISSING": -20,
            "CROP_NOT_FOUND": -20,
            "STAGE_NOT_FOUND": -10,
            "INVALID_DATE": -40,
            "MISSING_SOWING_DATE": -10,
            "SERVICE_FAILED_CROP_STAGE": -50,
            "SERVICE_FAILED_FERTILIZER": -20,
            "SERVICE_FAILED_IRRIGATION": -20,
            "SERVICE_FAILED_PEST": -20,
        }

    async def execute_pipeline(self, request: AdvisoryRequestDTO) -> AdvisoryDTO:
        start_time = time.time()
        correlation_id = str(uuid.uuid4())
        
        # Step 1: Validate Context & Initialize
        ctx = DecisionContextDTO(request=request)
        ctx.metadata.correlation_id = correlation_id
        ctx.execution_state = "STARTED"
        logger.info(f"[{correlation_id}] START PIPELINE")
        
        # Step 2: Load Rules
        ctx.rules_crop = self.rule_provider.get_crop_rules(request.crop)
        ctx.rules_irrigation = self.rule_provider.get_irrigation_rules(request.crop)
        ctx.rules_pest = self.rule_provider.get_pest_rules(request.crop)
        ctx.rules_fertilizer = self.rule_provider.get_fertilizer_rules(request.crop)
        logger.info(f"[{correlation_id}] DEPENDENCY LOADED: Rules")
        
        # Step 3: Load Weather
        ctx.weather = await self.weather_provider.get_weather(request.location)
        logger.info(f"[{correlation_id}] DEPENDENCY LOADED: Weather")
        
        # Step 4: Crop Stage (Sequential dependency)
        crop_req = CropStageRequestDTO(crop=request.crop, sowing_date=request.sowing_date, rules=ctx.rules_crop)
        ctx.out_crop_stage = ExecutionWrapper.execute(
            "CROP_STAGE", correlation_id, crop_stage_service.execute, 
            lambda: CropStageResponseDTO(stage="Unknown", days_active=0), crop_req
        )
        ctx.degradation_flags.extend(ctx.out_crop_stage.degradation_flags)
        
        # Step 5: Parallel Stage (Fertilizer, Irrigation, Pest)
        stage = ctx.out_crop_stage.stage
        
        fert_req = FertilizerRequestDTO(crop=request.crop, stage=stage, rules=ctx.rules_fertilizer)
        irr_req = IrrigationRequestDTO(stage=stage, weather=ctx.weather, rules=ctx.rules_irrigation)
        pest_req = PestRequestDTO(crop=request.crop, weather=ctx.weather, rules=ctx.rules_pest)
        
        # Executing concurrently via to_thread (since they are sync CPU bound) or just sequentially.
        # User requested architecture should support gather().
        async def run_fert():
            return ExecutionWrapper.execute(
                "FERTILIZER", correlation_id, fertilizer_service.execute, 
                lambda: FertilizerResponseDTO(n=0, p=0, k=0, notes="Fallback"), fert_req
            )
            
        async def run_irr():
            return ExecutionWrapper.execute(
                "IRRIGATION", correlation_id, irrigation_service.execute, 
                lambda: IrrigationResponseDTO(irrigate=False, volume_l=0, reason="Fallback"), irr_req
            )
            
        async def run_pest():
            return ExecutionWrapper.execute(
                "PEST", correlation_id, pest_service.execute, 
                lambda: PestResponseDTO(risk_level="Unknown", pests=[]), pest_req
            )
            
        ctx.out_fertilizer, ctx.out_irrigation, ctx.out_pest = await asyncio.gather(
            run_fert(), run_irr(), run_pest()
        )
        
        # Step 6: Aggregate
        ctx.degradation_flags.extend(ctx.out_fertilizer.degradation_flags)
        ctx.degradation_flags.extend(ctx.out_irrigation.degradation_flags)
        ctx.degradation_flags.extend(ctx.out_pest.degradation_flags)
        
        # Step 7: Confidence
        conf_req = ConfidenceRequestDTO(flags=ctx.degradation_flags, penalties=self.penalties)
        ctx.out_confidence = ExecutionWrapper.execute(
            "CONFIDENCE", correlation_id, confidence_service.execute, 
            lambda: ConfidenceResponseDTO(score=0), conf_req
        )
        logger.info(f"[{correlation_id}] CONFIDENCE: {ctx.out_confidence.score}")
        
        # Step 8: Build Advisory
        ctx.metadata.execution_time_ms = (time.time() - start_time) * 1000
        logger.info(f"[{correlation_id}] COMPLETE in {ctx.metadata.execution_time_ms:.2f}ms")
        
        return AdvisoryDTO(
            crop_stage=ctx.out_crop_stage,
            irrigation=ctx.out_irrigation,
            fertilizer=ctx.out_fertilizer,
            pest=ctx.out_pest,
            confidence=ctx.out_confidence,
            metadata=ctx.metadata
        )
