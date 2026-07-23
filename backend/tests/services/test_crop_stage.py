import unittest
from datetime import datetime, timedelta
from backend.models.dtos import CropStageRequestDTO, CropRulesDTO
from backend.services.crop_stage_service import execute, _calculate_days

class TestCropStageService(unittest.TestCase):
    def setUp(self):
        self.rules = CropRulesDTO(stages=[
            {"name": "vegetative", "min_days": 0, "max_days": 40},
            {"name": "flowering", "min_days": 41, "max_days": 70}
        ])

    def test_calculate_days(self):
        sowing = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")
        days = _calculate_days(sowing)
        self.assertEqual(days, 20)

    def test_happy_path(self):
        sowing = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")
        req = CropStageRequestDTO(crop="wheat", sowing_date=sowing, rules=self.rules)
        res = execute(req)
        self.assertEqual(res.stage, "vegetative")
        self.assertEqual(res.days_active, 20)
        self.assertEqual(res.degradation_flags, [])

    def test_invalid_date(self):
        req = CropStageRequestDTO(crop="wheat", sowing_date="invalid", rules=self.rules)
        res = execute(req)
        self.assertEqual(res.stage, "Unknown")
        self.assertIn("INVALID_DATE", res.degradation_flags)

    def test_missing_rule(self):
        sowing = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
        req = CropStageRequestDTO(crop="wheat", sowing_date=sowing, rules=self.rules)
        res = execute(req)
        self.assertIn("RULE_MISSING", res.degradation_flags)
