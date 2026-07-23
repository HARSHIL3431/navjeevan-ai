import json
import logging
from pathlib import Path
import httpx
from backend.models.dtos import (
    WeatherDTO, CropRulesDTO, IrrigationRulesDTO, 
    PestRulesDTO, FertilizerRulesDTO
)

logger = logging.getLogger(__name__)

import time

class WeatherProvider:
    """Provides weather data from an external API with caching."""
    def __init__(self):
        # Using Open-Meteo as a reliable free geocoding + weather API without keys
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.cache = {}
        self.cache_ttl = 1800 # 30 mins

    async def get_weather(self, location: str) -> WeatherDTO:
        location_key = location.lower().strip()
        now = time.time()
        
        if location_key in self.cache:
            entry = self.cache[location_key]
            if now - entry["time"] < self.cache_ttl:
                logger.info(f"Weather cache hit for {location_key}")
                return entry["data"]
                
        try:
            async with httpx.AsyncClient() as client:
                # 1. Geocode
                geo_resp = await client.get(self.geocoding_url, params={"name": location, "count": 1})
                geo_resp.raise_for_status()
                geo_data = geo_resp.json()
                
                if not geo_data.get("results"):
                    logger.warning(f"Weather geocoding failed for location: {location}")
                    return WeatherDTO(is_available=False)
                    
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
                
                # 2. Get Weather
                w_resp = await client.get(self.weather_url, params={
                    "latitude": lat, 
                    "longitude": lon, 
                    "current": "temperature_2m,relative_humidity_2m",
                    "daily": "precipitation_sum",
                    "forecast_days": 3
                })
                w_resp.raise_for_status()
                w_data = w_resp.json()
                
                temp = w_data["current"]["temperature_2m"]
                hum = w_data["current"]["relative_humidity_2m"]
                rain_sum = sum(w_data["daily"]["precipitation_sum"][:3]) # 3 day forecast sum
                
                dto = WeatherDTO(temp_c=temp, humidity_percent=hum, forecast_3d_rain_mm=rain_sum, is_available=True)
                self.cache[location_key] = {"data": dto, "time": now}
                return dto
                
        except Exception as e:
            logger.error(f"WeatherProvider HTTP error: {e}")
            return WeatherDTO(is_available=False)

class RuleProvider:
    """Provides business rules from JSON datasets."""
    def __init__(self, rules_path: str = "backend/data/rules.json"):
        self.rules_path = Path(rules_path)
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
