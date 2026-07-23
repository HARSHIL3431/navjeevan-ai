from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query, Request

from backend.decision_engine.providers import WeatherProvider
from backend.models.response_models import StandardResponse

router = APIRouter(prefix="/api/v1/weather", tags=["Weather"])


@router.get("", response_model=StandardResponse[dict])
async def get_weather(
    request: Request,
    location: str = Query(..., min_length=2, description="City or village name"),
):
    """
    Returns current weather conditions for a given location.
    Data sourced from Open-Meteo (no API key required).
    Cached for 30 minutes per location.
    """
    provider: WeatherProvider = request.app.state.weather_provider
    weather = await provider.get_weather(location)

    if not weather.is_available:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "message": f"Weather data unavailable for '{location}'. Try again shortly.",
            },
        )

    return StandardResponse(
        status="success",
        message="Weather data retrieved",
        data={
            "location": location,
            "temp_c": weather.temp_c,
            "humidity_percent": weather.humidity_percent,
            "forecast_3d_rain_mm": weather.forecast_3d_rain_mm,
            "source": "open-meteo",
            "cache_ttl_seconds": 1800,
        },
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
