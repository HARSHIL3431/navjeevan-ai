import unittest
import asyncio
from unittest.mock import patch, MagicMock
from backend.models.dtos import AdvisoryRequestDTO, WeatherDTO
from backend.decision_engine.providers import WeatherProvider, RuleProvider
from backend.decision_engine.advisory_engine import AdvisoryEngine

class TestAdvisoryEngine(unittest.TestCase):
    def setUp(self):
        self.weather_provider = WeatherProvider()
        self.rule_provider = RuleProvider()
        self.engine = AdvisoryEngine(self.weather_provider, self.rule_provider)

    def test_happy_path(self):
        req = AdvisoryRequestDTO(crop="wheat", location="surat", sowing_date="2024-01-01")
        result = asyncio.run(self.engine.execute_pipeline(req))
        
        self.assertIsNotNone(result.metadata.correlation_id)
        self.assertGreater(result.metadata.execution_time_ms, 0)
        self.assertGreater(result.confidence.score, 0)
        self.assertEqual(result.crop_stage.stage, "Mature")

    @patch('backend.decision_engine.providers.WeatherProvider.get_weather')
    def test_weather_missing(self, mock_get_weather):
        async def mock_weather(*args, **kwargs):
            return WeatherDTO(is_available=False)
        mock_get_weather.side_effect = mock_weather
        
        req = AdvisoryRequestDTO(crop="wheat", location="surat", sowing_date="2024-01-01")
        result = asyncio.run(self.engine.execute_pipeline(req))
        
        # Degradation flags from Weather should cause penalty
        self.assertIn("WEATHER_UNAVAILABLE", result.pest.degradation_flags)
        self.assertTrue(result.confidence.score < 100)

    @patch('backend.services.pest_service.execute')
    def test_service_exception(self, mock_pest_execute):
        # Force a service crash
        mock_pest_execute.side_effect = Exception("Simulated service crash")
        
        req = AdvisoryRequestDTO(crop="wheat", location="surat", sowing_date="2024-01-01")
        result = asyncio.run(self.engine.execute_pipeline(req))
        
        # Engine should catch it via Wrapper and append degradation flag
        self.assertIn("SERVICE_FAILED_PEST", result.pest.degradation_flags)
        self.assertEqual(result.pest.risk_level, "Unknown") # Fallback value
        self.assertTrue(result.confidence.score < 100)
