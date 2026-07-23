from fastapi import APIRouter, Depends, Request
from datetime import datetime, timezone
import dataclasses
from backend.models.request_models import AdvisoryRequest
from backend.models.response_models import StandardResponse, AdvisoryResponsePayload
from backend.models.dtos import AdvisoryRequestDTO
from backend.decision_engine.advisory_engine import AdvisoryEngine
from backend.decision_engine.providers import WeatherProvider, RuleProvider
from backend.services.ai_formatter import AIFormatterService

router = APIRouter(prefix="/api/v1/advisory", tags=["Advisory"])


def get_weather_provider(request: Request) -> WeatherProvider:
    # Use singleton from app.state so cache persists across requests
    return request.app.state.weather_provider


def get_rule_provider(request: Request) -> RuleProvider:
    return request.app.state.rule_provider


def get_advisory_engine(
    weather: WeatherProvider = Depends(get_weather_provider),
    rules: RuleProvider = Depends(get_rule_provider)
) -> AdvisoryEngine:
    return AdvisoryEngine(weather_provider=weather, rule_provider=rules)


def get_ai_formatter() -> AIFormatterService:
    return AIFormatterService()


@router.post("", response_model=StandardResponse[AdvisoryResponsePayload])
async def get_advisory(
    request: AdvisoryRequest,
    engine: AdvisoryEngine = Depends(get_advisory_engine),
    ai_formatter: AIFormatterService = Depends(get_ai_formatter)
):
    req_dto = AdvisoryRequestDTO(
        crop=request.crop,
        location=request.location,
        sowing_date=request.sowing_date
    )

    advisory_dto = await engine.execute_pipeline(req_dto)
    ai_advice = await ai_formatter.format_advisory(advisory_dto)

    payload = AdvisoryResponsePayload(
        decision_data=dataclasses.asdict(advisory_dto),
        ai_advice=ai_advice
    )

    return StandardResponse(
        status="success",
        message="Advisory generated successfully",
        data=payload,
        timestamp=datetime.now(timezone.utc).isoformat()  # fixed: was datetime.UTC
    )
