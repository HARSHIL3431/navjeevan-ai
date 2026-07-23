import unittest
from fastapi.testclient import TestClient
from backend.main import app
import httpx

class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "service": "navjeevan-ai-backend"})

    def test_advisory_endpoint(self):
        payload = {
            "crop": "wheat",
            "location": "Pune",
            "sowing_date": "2024-01-01"
        }
        # This will test the entire stack: Route -> Engine -> Providers (Open-Meteo) -> AI Formatter (Groq/Mocked)
        response = self.client.post("/api/v1/advisory", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("data", data)
        
        payload_data = data["data"]
        self.assertIn("ai_advice", payload_data)
        self.assertIn("decision_data", payload_data)
        
        decision_data = payload_data["decision_data"]
        self.assertIn("confidence", decision_data)
        self.assertIn("metadata", decision_data)
        
        # Verify provider integration successfully pulled data
        self.assertGreaterEqual(decision_data["confidence"]["score"], 0)
