import unittest
from backend.models.dtos import FertilizerRequestDTO, FertilizerRulesDTO
from backend.services.fertilizer_service import execute

class TestFertilizerService(unittest.TestCase):
    def setUp(self):
        self.rules = FertilizerRulesDTO(requirements={
            "wheat": {
                "vegetative": {"N": 50, "P": 20, "K": 10, "notes": "Apply near roots"},
                "flowering": {"N": 20, "P": 40, "K": 30, "notes": "Foliar spray"}
            }
        })

    def test_happy_path(self):
        req = FertilizerRequestDTO(crop="wheat", stage="vegetative", rules=self.rules)
        res = execute(req)
        self.assertEqual(res.n, 50)
        self.assertEqual(res.p, 20)
        self.assertEqual(res.k, 10)
        self.assertEqual(res.degradation_flags, [])

    def test_unknown_crop(self):
        req = FertilizerRequestDTO(crop="rice", stage="vegetative", rules=self.rules)
        res = execute(req)
        self.assertEqual(res.n, 0)
        self.assertIn("CROP_NOT_FOUND", res.degradation_flags)

    def test_unknown_stage(self):
        req = FertilizerRequestDTO(crop="wheat", stage="harvest", rules=self.rules)
        res = execute(req)
        # Should fallback to vegetative (first stage)
        self.assertEqual(res.n, 50)
        self.assertIn("STAGE_NOT_FOUND", res.degradation_flags)
