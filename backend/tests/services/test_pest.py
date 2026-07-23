import unittest
from backend.models.dtos import PestRequestDTO, PestRulesDTO, WeatherDTO
from backend.services.pest_service import execute

class TestPestService(unittest.TestCase):
    def setUp(self):
        self.rules = PestRulesDTO(pests=[
            {"name": "Aphids", "min_temp": 20, "max_temp": 30, "min_humidity": 70}
        ])

    def test_high_risk(self):
        weather = WeatherDTO(temp_c=25, humidity_percent=75)
        req = PestRequestDTO(crop="wheat", weather=weather, rules=self.rules)
        res = execute(req)
        self.assertEqual(res.risk_level, "High")
        self.assertIn("Aphids", res.pests)

    def test_low_risk(self):
        weather = WeatherDTO(temp_c=15, humidity_percent=50)
        req = PestRequestDTO(crop="wheat", weather=weather, rules=self.rules)
        res = execute(req)
        self.assertEqual(res.risk_level, "Low")
        self.assertEqual(res.pests, [])

    def test_weather_unavailable(self):
        weather = WeatherDTO(is_available=False)
        req = PestRequestDTO(crop="wheat", weather=weather, rules=self.rules)
        res = execute(req)
        self.assertEqual(res.risk_level, "Unknown")
        self.assertIn("WEATHER_UNAVAILABLE", res.degradation_flags)
