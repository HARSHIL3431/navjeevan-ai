import json
import asyncio
import logging
from pathlib import Path
import httpx
from backend.models.dtos import (
    WeatherDTO, CropRulesDTO, IrrigationRulesDTO,
    PestRulesDTO, FertilizerRulesDTO
)
from backend.config.settings import settings

logger = logging.getLogger(__name__)

import time

_MAX_RETRIES = 3
_RETRY_DELAY_SECONDS = 1.0


class WeatherProvider:
    """
    Fetches weather data using OpenWeatherMap (primary) with Open-Meteo as fallback.
    Results are cached per location for 30 minutes.
    """
    def __init__(self):
        self.owm_url = "https://api.openweathermap.org/data/2.5/weather"
        self.owm_forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        # Open-Meteo fallback (no key needed)
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.openmeteo_url = "https://api.open-meteo.com/v1/forecast"
        self.cache: dict = {}
        self.cache_ttl = 1800  # 30 mins

    async def get_weather(self, location: str) -> WeatherDTO:
        location_key = location.lower().strip()
        now = time.time()

        if location_key in self.cache:
            entry = self.cache[location_key]
            if now - entry["time"] < self.cache_ttl:
                logger.info("Weather cache hit for %s", location_key)
                return entry["data"]

        dto = await self._fetch_with_retry(location, location_key)
        if dto.is_available:
            self.cache[location_key] = {"data": dto, "time": now}
        return dto

    async def _fetch_with_retry(self, location: str, location_key: str) -> WeatherDTO:
        last_error: Exception | None = None
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                return await self._fetch(location)
            except Exception as exc:
                last_error = exc
                logger.warning(
                    "WeatherProvider attempt %d/%d failed for %s: %s",
                    attempt, _MAX_RETRIES, location_key, exc
                )
                if attempt < _MAX_RETRIES:
                    await asyncio.sleep(_RETRY_DELAY_SECONDS * attempt)

        logger.error("WeatherProvider exhausted retries for %s: %s", location_key, last_error)
        return WeatherDTO(is_available=False)

    async def _fetch(self, location: str) -> WeatherDTO:
        api_key = settings.openweather_api_key.strip()
        if api_key and api_key != "your_openweathermap_api_key_here":
            return await self._fetch_openweathermap(location, api_key)
        logger.info("No OpenWeatherMap key set — using Open-Meteo fallback")
        return await self._fetch_openmeteo(location)

    async def _fetch_openweathermap(self, location: str, api_key: str) -> WeatherDTO:
        """Primary: OpenWeatherMap current weather + 3-day rainfall forecast."""
        async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
            # Current weather
            resp = await client.get(self.owm_url, params={
                "q": location,
                "appid": api_key,
                "units": "metric",
            })
            resp.raise_for_status()
            data = resp.json()

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            rain_1h = data.get("rain", {}).get("1h", 0.0)

            # 3-day forecast for rainfall sum
            forecast_resp = await client.get(self.owm_forecast_url, params={
                "q": location,
                "appid": api_key,
                "units": "metric",
                "cnt": 24,  # 24 x 3hr slots = 3 days
            })
            forecast_resp.raise_for_status()
            forecast_data = forecast_resp.json()

            rain_3d = sum(
                entry.get("rain", {}).get("3h", 0.0)
                for entry in forecast_data.get("list", [])
            )

            logger.info("OpenWeatherMap data fetched for %s: %.1f°C, %d%% humidity", location, temp, humidity)
            return WeatherDTO(
                temp_c=temp,
                humidity_percent=float(humidity),
                forecast_3d_rain_mm=rain_3d,
                is_available=True,
            )

    async def _fetch_openmeteo(self, location: str) -> WeatherDTO:
        """Fallback: Open-Meteo (no API key required)."""
        async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
            geo_resp = await client.get(
                self.geocoding_url, params={"name": location, "count": 1}
            )
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()

            if not geo_data.get("results"):
                logger.warning("Open-Meteo geocoding returned no results for: %s", location)
                return WeatherDTO(is_available=False)

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]

            w_resp = await client.get(self.openmeteo_url, params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m",
                "daily": "precipitation_sum",
                "forecast_days": 3,
            })
            w_resp.raise_for_status()
            w_data = w_resp.json()

            temp = w_data["current"]["temperature_2m"]
            hum = w_data["current"]["relative_humidity_2m"]
            rain_sum = sum(w_data["daily"]["precipitation_sum"][:3])

            logger.info("Open-Meteo data fetched for %s: %.1f°C, %.1f%% humidity", location, temp, hum)
            return WeatherDTO(
                temp_c=temp,
                humidity_percent=hum,
                forecast_3d_rain_mm=rain_sum,
                is_available=True,
            )

class RuleProvider:
    """Provides business rules from JSON datasets."""
    def __init__(self, rules_path: str | None = None):
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            # Anchor relative to this file — works regardless of working directory
            self.rules_path = Path(__file__).resolve().parents[1] / "data" / "rules.json"
        self.rules = self._load_rules()

    def _load_rules(self) -> dict:
        if not self.rules_path.exists():
            logger.error(f"Rules file not found at {self.rules_path}")
            return {}
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error parsing rules JSON: {e}")
            return {}

    def _get_crop_data(self, crop: str) -> dict:
        return self.rules.get(crop.lower(), {})

    def get_crop_rules(self, crop: str) -> CropRulesDTO:
        data = self._get_crop_data(crop).get("crop_stage", {})
        return CropRulesDTO(stages=data.get("stages", []))
        
    def get_irrigation_rules(self, crop: str) -> IrrigationRulesDTO:
        data = self._get_crop_data(crop).get("irrigation", {})
        return IrrigationRulesDTO(
            rain_threshold_mm=data.get("rain_threshold_mm", 10.0), 
            stage_modifiers=data.get("stage_modifiers", {})
        )
        
    def get_pest_rules(self, crop: str) -> PestRulesDTO:
        data = self._get_crop_data(crop).get("pest", {})
        return PestRulesDTO(pests=data.get("pests", []))
        
    def get_fertilizer_rules(self, crop: str) -> FertilizerRulesDTO:
        data = self._get_crop_data(crop).get("fertilizer", {})
        return FertilizerRulesDTO(requirements=data.get("requirements", {}))
