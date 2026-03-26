import json
import logging
from typing import Any, Dict, Optional
from urllib import parse, request
from urllib.error import HTTPError, URLError

from backend.config.settings import settings

AGMARKNET_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
logger = logging.getLogger(__name__)


def _safe_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def _fetch_records(url: str) -> Optional[list]:
    attempt = 0
    while attempt < 2:
        attempt += 1
        try:
            req = request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "application/json",
                },
                method="GET",
            )
            with request.urlopen(req, timeout=settings.external_api_timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
            records = payload.get("records", [])
            if isinstance(records, list) and records:
                return records
            if attempt < 2:
                continue
            return []
        except TimeoutError:
            if attempt < 2:
                continue
            return None
        except HTTPError as error:
            logger.warning("Realtime API http error: %s", error)
            return None
        except URLError as error:
            logger.warning("Realtime API url error: %s", error)
            if attempt < 2:
                continue
            return None
        except Exception:
            logger.exception("Realtime API unexpected error")
            if attempt < 2:
                continue
            return None
    return None


def fetch_realtime_market_price(crop: str, location: str) -> Optional[Dict[str, Any]]:
    commodity = (crop or "").strip().title()
    district = (location or "").strip().title()

    if not commodity or not district:
        return None

    api_key = settings.data_gov_api_key.strip()
    if not api_key:
        logger.info("DATA_GOV_API_KEY missing; skipping realtime fetch")
        return None

    params = {
        "api-key": api_key,
        "format": "json",
        "limit": "100",
        "filters[commodity]": commodity,
    }
    url = f"{AGMARKNET_URL}?{parse.urlencode(params)}"

    records = _fetch_records(url)
    if records is None or not isinstance(records, list) or not records:
        return None

    filtered = [
        item for item in records if district.lower() in str(item.get("district", "")).lower()
    ]
    if not filtered:
        return None

    best = max(filtered, key=lambda row: _safe_int(row.get("modal_price")) or 0)
    price = _safe_int(best.get("modal_price"))
    if price is None:
        price = _safe_int(best.get("max_price"))
    if price is None:
        return None

    return {
        "market_name": str(best.get("market") or "N/A"),
        "location": str(best.get("district") or district),
        "state": str(best.get("state") or "N/A"),
        "price_per_qtl": price,
        "date": str(best.get("arrival_date") or "N/A"),
        "source": "Agmarknet API",
    }
