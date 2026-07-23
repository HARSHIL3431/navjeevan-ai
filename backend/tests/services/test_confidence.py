import unittest
from backend.models.dtos import ConfidenceRequestDTO
from backend.services.confidence_service import execute

class TestConfidenceService(unittest.TestCase):
    def setUp(self):
        self.penalties = {
            "WEATHER_UNAVAILABLE": -30,
            "RULE_MISSING": -20,
            "ESTIMATED_STAGE": -10,
            "INVALID_DATE": -40
        }

    def test_perfect_score(self):
        req = ConfidenceRequestDTO(flags=[], penalties=self.penalties)
        res = execute(req)
        self.assertEqual(res.score, 100)

    def test_single_penalty(self):
        req = ConfidenceRequestDTO(flags=["RULE_MISSING"], penalties=self.penalties)
        res = execute(req)
        self.assertEqual(res.score, 80)

    def test_multiple_penalties(self):
        req = ConfidenceRequestDTO(flags=["WEATHER_UNAVAILABLE", "ESTIMATED_STAGE"], penalties=self.penalties)
        res = execute(req)
        self.assertEqual(res.score, 60)

    def test_floor_zero(self):
        req = ConfidenceRequestDTO(flags=["WEATHER_UNAVAILABLE", "RULE_MISSING", "INVALID_DATE", "INVALID_DATE"], penalties=self.penalties)
        res = execute(req)
        self.assertEqual(res.score, 0) # 100 - 30 - 20 - 40 - 40 = -30 -> floor at 0
