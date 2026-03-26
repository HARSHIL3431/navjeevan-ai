import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)
FALLBACK_MESSAGE = "Sorry, I don't have this info. Please contact your local Krishi office."


def _contains(text: str, value: str) -> bool:
    return value.lower() in text.lower()


def _first_or_none(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return items[0] if items else {}


def _finalize_response(text: str) -> str:
    words = text.split()
    if len(words) <= 120:
        return text
    return " ".join(words[:120]).rstrip() + "..."


def _entity_matches(item: Dict[str, Any], entities: Dict[str, str]) -> bool:
    crop = (entities.get("crop") or "").lower()
    location = (entities.get("location") or "").lower()
    crop_ok = not crop or crop in str(item.get("crop", "")).lower()
    location_ok = not location or location in str(item.get("city", "")).lower()
    return crop_ok and location_ok


def handle_contact(query: str, contacts: List[Dict[str, Any]], entities: Dict[str, str]) -> str:
    try:
        if not contacts:
            return FALLBACK_MESSAGE

        q = (query or "").lower()
        entity_matches = [item for item in contacts if _entity_matches(item, entities)]
        matches = [
            item
            for item in contacts
            if _contains(q, str(item.get("crop", ""))) or _contains(q, str(item.get("city", "")))
        ]
        target = _first_or_none(entity_matches) or _first_or_none(matches) or _first_or_none(contacts)
        if not target:
            return FALLBACK_MESSAGE

        return _finalize_response(
            "CONTACTS:\n"
            f"Trader: {target.get('name', 'N/A')}\n"
            f"Phone: {target.get('phone', 'N/A')}\n"
            f"Location: {target.get('city', 'N/A')}\n"
            f"Notes: {target.get('notes', 'Call before visiting.')}"
        )
    except Exception:
        logger.exception("contact service failed")
        return FALLBACK_MESSAGE
