from dataclasses import dataclass, field
from typing import Optional, List, Dict

@dataclass
class WeatherDTO:
    temp_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    forecast_3d_rain_mm: Optional[float] = None
    is_available: bool = True

@dataclass
class CropRulesDTO:
    stages: List[Dict] = field(default_factory=list)

@dataclass
class IrrigationRulesDTO:
    rain_threshold_mm: float = 10.0
    stage_modifiers: Dict[str, float] = field(default_factory=dict)

@dataclass
class PestRulesDTO:
    pests: List[Dict] = field(default_factory=list)

@dataclass
class FertilizerRulesDTO:
    requirements: Dict[str, Dict] = field(default_factory=dict)

@dataclass
class CropStageRequestDTO:
    crop: str
    sowing_date: Optional[str]
    rules: CropRulesDTO

@dataclass
class CropStageResponseDTO:
    stage: str
    days_active: int
    degradation_flags: List[str] = field(default_factory=list)

@dataclass
class IrrigationRequestDTO:
    stage: str
    weather: WeatherDTO
    rules: IrrigationRulesDTO

@dataclass
class IrrigationResponseDTO:
    irrigate: bool
    volume_l: float
    reason: str
    degradation_flags: List[str] = field(default_factory=list)

@dataclass
class PestRequestDTO:
    crop: str
    weather: WeatherDTO
    rules: PestRulesDTO

@dataclass
class PestResponseDTO:
    risk_level: str
    pests: List[str]
    degradation_flags: List[str] = field(default_factory=list)

@dataclass
class FertilizerRequestDTO:
    crop: str
    stage: str
    rules: FertilizerRulesDTO

@dataclass
class FertilizerResponseDTO:
    n: float
    p: float
    k: float
    notes: str
    degradation_flags: List[str] = field(default_factory=list)

@dataclass
class ConfidenceRequestDTO:
    flags: List[str]
    penalties: Dict[str, int]

@dataclass
class ConfidenceResponseDTO:
    score: int


@dataclass
class AdvisoryMetadataDTO:
    correlation_id: str
    rule_version: str
    engine_version: str
    execution_time_ms: float
    weather_source: str
    weather_cached: bool
    fallback_used: bool

@dataclass
class AdvisoryDTO:
    crop_stage: Optional[CropStageResponseDTO] = None
    irrigation: Optional[IrrigationResponseDTO] = None
    fertilizer: Optional[FertilizerResponseDTO] = None
    pest: Optional[PestResponseDTO] = None
    confidence: Optional[ConfidenceResponseDTO] = None
    metadata: Optional[AdvisoryMetadataDTO] = None


@dataclass
class AdvisoryRequestDTO:
    crop: str
    location: str
    sowing_date: Optional[str] = None

@dataclass
class DecisionContextDTO:
    request: AdvisoryRequestDTO
    weather: Optional[WeatherDTO] = None
    rules_crop: Optional[CropRulesDTO] = None
    rules_irrigation: Optional[IrrigationRulesDTO] = None
    rules_fertilizer: Optional[FertilizerRulesDTO] = None
    rules_pest: Optional[PestRulesDTO] = None
    
    out_crop_stage: Optional[CropStageResponseDTO] = None
    out_irrigation: Optional[IrrigationResponseDTO] = None
    out_fertilizer: Optional[FertilizerResponseDTO] = None
    out_pest: Optional[PestResponseDTO] = None
    out_confidence: Optional[ConfidenceResponseDTO] = None
    
    degradation_flags: List[str] = field(default_factory=list)
    metadata: AdvisoryMetadataDTO = field(default_factory=lambda: AdvisoryMetadataDTO(
        correlation_id='', rule_version='1.0', engine_version='1.0', execution_time_ms=0.0,
        weather_source='None', weather_cached=False, fallback_used=False
    ))
    execution_state: str = 'INITIALIZED'
