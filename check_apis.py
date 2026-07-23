"""
API Key Health Checker
Run: python check_apis.py
"""
import asyncio
import httpx
import warnings
warnings.filterwarnings("ignore")  # suppress SSL warnings

from dotenv import load_dotenv
import os

load_dotenv()

OWM_KEY      = os.getenv("OPENWEATHER_API_KEY", "")
DATA_GOV_KEY = os.getenv("DATA_GOV_API_KEY", "")
GROQ_KEY     = os.getenv("GROQ_API_KEY", "")

LOCATION = "surat"


async def check_openweathermap(client: httpx.AsyncClient):
    print("\n=== OpenWeatherMap ===")
    print(f"Key: {OWM_KEY[:8]}...{OWM_KEY[-4:]}")

    if not OWM_KEY:
        print("❌ Key missing in .env")
        return

    # Current weather
    try:
        r = await client.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": LOCATION, "appid": OWM_KEY, "units": "metric"},
        )
        if r.status_code == 200:
            d = r.json()
            print(f"✅ Current weather OK")
            print(f"   Temp     : {d['main']['temp']} °C")
            print(f"   Humidity : {d['main']['humidity']} %")
            print(f"   Rain 1h  : {d.get('rain', {}).get('1h', 0.0)} mm")
            print(f"   City     : {d.get('name')}, {d.get('sys', {}).get('country')}")
        elif r.status_code == 401:
            print("❌ Invalid API key (401 Unauthorized)")
        elif r.status_code == 429:
            print("⚠️  Rate limit exceeded (429)")
        else:
            print(f"❌ Unexpected status {r.status_code}: {r.text[:150]}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

    # 3-day forecast
    try:
        r2 = await client.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={"q": LOCATION, "appid": OWM_KEY, "units": "metric", "cnt": 24},
        )
        if r2.status_code == 200:
            slots = r2.json().get("list", [])
            rain_3d = sum(s.get("rain", {}).get("3h", 0.0) for s in slots)
            print(f"✅ Forecast OK — 3-day rain: {rain_3d:.1f} mm ({len(slots)} slots)")
        else:
            print(f"❌ Forecast failed {r2.status_code}: {r2.text[:150]}")
    except Exception as e:
        print(f"❌ Forecast request failed: {e}")


async def check_open_meteo(client: httpx.AsyncClient):
    print("\n=== Open-Meteo (no key needed) ===")
    try:
        geo = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": LOCATION, "count": 1},
        )
        geo.raise_for_status()
        results = geo.json().get("results", [])
        if not results:
            print(f"❌ Geocoding returned no results for '{LOCATION}'")
            return
        lat, lon = results[0]["latitude"], results[0]["longitude"]
        print(f"✅ Geocoding OK — lat:{lat}, lon:{lon}")

        w = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m",
                "daily": "precipitation_sum",
                "forecast_days": 3,
            },
        )
        w.raise_for_status()
        wd = w.json()
        temp = wd["current"]["temperature_2m"]
        hum  = wd["current"]["relative_humidity_2m"]
        rain = sum(wd["daily"]["precipitation_sum"][:3])
        print(f"✅ Weather OK — Temp: {temp}°C, Humidity: {hum}%, Rain 3d: {rain:.1f}mm")
    except Exception as e:
        print(f"❌ Open-Meteo failed: {e}")


async def check_data_gov(client: httpx.AsyncClient):
    print("\n=== Data.gov.in ===")
    print(f"Key: {DATA_GOV_KEY[:8]}...{DATA_GOV_KEY[-4:]}" if DATA_GOV_KEY else "Key: missing")

    if not DATA_GOV_KEY:
        print("❌ Key missing in .env")
        return

    try:
        r = await client.get(
            "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070",
            params={"api-key": DATA_GOV_KEY, "format": "json", "limit": 1},
            timeout=10.0,
        )
        if r.status_code == 200:
            print(f"✅ Data.gov.in OK")
            print(f"   Response snippet: {r.text[:150]}")
        elif r.status_code == 403:
            print("❌ Invalid/expired key (403 Forbidden)")
        else:
            print(f"❌ Status {r.status_code}: {r.text[:150]}")
    except httpx.TimeoutException:
        print("❌ Timed out — api.data.gov.in unreachable from your network")
    except Exception as e:
        print(f"❌ Request failed: {e}")


async def check_groq(client: httpx.AsyncClient):
    print("\n=== Groq ===")
    print(f"Key: {GROQ_KEY[:8]}...{GROQ_KEY[-4:]}" if GROQ_KEY else "Key: missing")

    if not GROQ_KEY:
        print("❌ Key missing in .env")
        return

    try:
        r = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": "Say OK"}],
                "max_tokens": 5,
            },
        )
        if r.status_code == 200:
            reply = r.json()["choices"][0]["message"]["content"]
            print(f"✅ Groq OK — Model reply: '{reply.strip()}'")
        elif r.status_code == 401:
            print("❌ Invalid API key (401)")
        elif r.status_code == 429:
            print("⚠️  Rate limit exceeded (429)")
        else:
            print(f"❌ Status {r.status_code}: {r.text[:150]}")
    except Exception as e:
        print(f"❌ Groq request failed: {e}")


async def main():
    print("=" * 40)
    print("  API Key Health Check")
    print("=" * 40)
    async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
        await check_openweathermap(client)
        await check_open_meteo(client)
        await check_data_gov(client)
        await check_groq(client)
    print("\n" + "=" * 40)


if __name__ == "__main__":
    asyncio.run(main())
