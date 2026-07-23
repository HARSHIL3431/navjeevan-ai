import unittest
from backend.models.dtos import IrrigationRequestDTO, IrrigationRulesDTO, WeatherDTO
from backend.services.irrigation_service import execute

class TestIrrigationService(unittest.TestCase):
    def setUp(self):
        self.rules = IrrigationRulesDTO(rain_threshold_mm=10.0, stage_modifiers={"flowering": 1.5})

    def test_happy_path_dry(self):
        weather = WeatherDTO(forecast_3d_rain_mm=0.0)
        req = IrrigationRequestDTO(stage="flowering", weather=weather, rules=self.rules)
        res = execute(req)
        self.assertTrue(res.irrigate)
        self.assertEqual(res.volume_l, 1500.0)
        self.assertEqual(res.degradation_flags, [])

    def test_rain_expected(self):
        weather = WeatherDTO(forecast_3d_rain_mm=15.0)
        req = IrrigationRequestDTO(stage="vegetative", weather=weather, rules=self.rules)
        res = execute(req)
        self.assertFalse(res.irrigate)
        self.assertEqual(res.volume_l, 0.0)

    def test_weather_unavailable(self):
        weather = WeatherDTO(is_available=False)
        req = IrrigationRequestDTO(stage="vegetative", weather=weather, rules=self.rules)
        res = execute(req)
        self.assertTrue(res.irrigate)
        self.assertIn("WEATHER_UNAVAILABLE", res.degradation_flags)
