import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.decision_engine.providers import WeatherProvider
from backend.models.dtos import WeatherDTO


def _make_mock_client(geo_results, weather_data):
    """Build a mock httpx.AsyncClient that returns preset responses."""
    geo_response = MagicMock()
    geo_response.raise_for_status = MagicMock()
    geo_response.json.return_value = geo_results

    weather_response = MagicMock()
    weather_response.raise_for_status = MagicMock()
    weather_response.json.return_value = weather_data

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=[geo_response, weather_response])
    return mock_client


GEO_RESULTS = {"results": [{"latitude": 21.17, "longitude": 72.83}]}
WEATHER_DATA = {
    "current": {"temperature_2m": 32.5, "relative_humidity_2m": 78.0},
    "daily": {"precipitation_sum": [2.0, 0.0, 5.0]},
}


class TestWeatherProvider(unittest.TestCase):

    def setUp(self):
        self.provider = WeatherProvider()

    def test_happy_path_returns_correct_dto(self):
        mock_client = _make_mock_client(GEO_RESULTS, WEATHER_DATA)
        with patch("httpx.AsyncClient", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_client), __aexit__=AsyncMock())):
            result = asyncio.run(self.provider.get_weather("surat"))

        self.assertTrue(result.is_available)
        self.assertEqual(result.temp_c, 32.5)
        self.assertEqual(result.humidity_percent, 78.0)
        self.assertAlmostEqual(result.forecast_3d_rain_mm, 7.0)

    def test_cache_hit_skips_http(self):
        import time
        dto = WeatherDTO(temp_c=30.0, humidity_percent=70.0, forecast_3d_rain_mm=5.0, is_available=True)
        self.provider.cache["surat"] = {"data": dto, "time": time.time()}

        with patch("httpx.AsyncClient") as mock_http:
            result = asyncio.run(self.provider.get_weather("surat"))
            mock_http.assert_not_called()

        self.assertEqual(result.temp_c, 30.0)

    def test_geocoding_no_results_returns_unavailable(self):
        mock_client = _make_mock_client({"results": []}, {})
        with patch("httpx.AsyncClient", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_client), __aexit__=AsyncMock())):
            result = asyncio.run(self.provider.get_weather("unknown_place"))

        self.assertFalse(result.is_available)

    def test_http_failure_returns_unavailable_after_retries(self):
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=Exception("Connection refused"))

        with patch("httpx.AsyncClient", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_client), __aexit__=AsyncMock())):
            with patch("asyncio.sleep", new_callable=AsyncMock):  # skip retry delays in tests
                result = asyncio.run(self.provider.get_weather("surat"))

        self.assertFalse(result.is_available)

    def test_failed_fetch_not_cached(self):
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(side_effect=Exception("Timeout"))

        with patch("httpx.AsyncClient", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_client), __aexit__=AsyncMock())):
            with patch("asyncio.sleep", new_callable=AsyncMock):
                asyncio.run(self.provider.get_weather("surat"))

        self.assertNotIn("surat", self.provider.cache)


class TestWeatherEndpoint(unittest.TestCase):
    """Integration tests for GET /api/v1/weather"""

    def setUp(self):
        from fastapi.testclient import TestClient
        from backend.main import app
        self.client = TestClient(app)

    def test_valid_location_returns_200(self):
        import time
        from backend.models.dtos import WeatherDTO
        dto = WeatherDTO(temp_c=30.0, humidity_percent=65.0, forecast_3d_rain_mm=3.0, is_available=True)
        self.client.app.state.weather_provider.cache["surat"] = {"data": dto, "time": time.time()}

        response = self.client.get("/api/v1/weather?location=surat")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["temp_c"], 30.0)

    def test_missing_location_param_returns_422(self):
        response = self.client.get("/api/v1/weather")
        self.assertEqual(response.status_code, 422)

    def test_short_location_returns_422(self):
        response = self.client.get("/api/v1/weather?location=a")
        self.assertEqual(response.status_code, 422)
