import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)
FALLBACK_MESSAGE = "Sorry, I don't have this info. Please contact your local Krishi office."


def _contains(text: str, value: str) -> bool:
    return value.lower() in text.lower()


def _finalize_response(text: str) -> str:
    words = text.split()
    if len(words) <= 120:
        return text
    return " ".join(words[:120]).rstrip() + "..."


def handle_mandi(query: str, mandis: List[Dict[str, Any]], entities: Dict[str, str]) -> str:
    try:
        if not mandis:
            return FALLBACK_MESSAGE

        q = (query or "").lower()
        location = (entities.get("location") or "").lower()
        matches = [item for item in mandis if location and location in str(item.get("city", "")).lower()]
        if not matches:
            matches = [item for item in mandis if _contains(q, str(item.get("city", "")))]
        selected = matches[:2] if matches else mandis[:2]
        if not selected:
            return FALLBACK_MESSAGE

        lines = ["MANDI:"]
        for idx, mandi in enumerate(selected, start=1):
            lines.append(
                f"{idx}. {mandi.get('mandi_name', 'N/A')} ({mandi.get('city', 'N/A')}) - "
                f"{mandi.get('distance_km', 'N/A')} km, {mandi.get('timings', 'N/A')}, "
                f"Crops: {', '.join(mandi.get('crops', [])) or 'N/A'}"
            )
        return _finalize_response("\n".join(lines))
    except Exception:
        logger.exception("mandi service failed")
        return FALLBACK_MESSAGE
