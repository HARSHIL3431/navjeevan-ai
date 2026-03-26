import logging
from typing import Any, Dict

from backend.services.contact_service import FALLBACK_MESSAGE as CONTACT_FALLBACK
from backend.services.contact_service import handle_contact
from backend.services.data_service import ensure_data_loaded, get_all_data
from backend.services.document_service import handle_document
from backend.services.intent_service import detect_intent, extract_entities, parse_query
from backend.services.mandi_service import handle_mandi
from backend.services.market_service import handle_market
from backend.services.scheme_service import handle_scheme

logger = logging.getLogger(__name__)
FALLBACK_MESSAGE = CONTACT_FALLBACK


def _resolve_intent(query: str, parsed: Dict[str, Any]) -> str:
    query_type = str(parsed.get("query_type") or "").lower()
    locations = parsed.get("locations") or []
    if not isinstance(locations, list):
        locations = []
    q = (query or "").lower()

    if "compare" in q and any(token in q for token in ["price", "prices", "rate", "rates", "bhav", "msp"]):
        return "market"

    if "compare" in q and len(locations) >= 2:
        return "market"

    if query_type == "price":
        return "market"
    if query_type == "mandi":
        return "mandi"
    if query_type == "scheme":
        return "scheme"

    if any(token in q for token in ["document", "documents", "docs", "paper", "papers", "checklist", "kcc"]):
        return "document"
    if any(token in q for token in ["trader", "buyer", "contact", "phone", "number", "dealer"]):
        return "contact"

    return detect_intent(query)


def process_chat_query(query: str) -> Dict[str, Any]:
    try:
        logger.info("Incoming query: %s", query)
        ensure_data_loaded()
        data = get_all_data()

        parsed = parse_query(query)
        intent = _resolve_intent(query, parsed)
        logger.info("Detected intent: %s", intent)

        entities = extract_entities(query)
        entities["crop"] = parsed.get("crop") or entities.get("crop", "")
        entities["location"] = parsed.get("location") or entities.get("location", "")
        entities["locations"] = parsed.get("locations") or ([entities.get("location")] if entities.get("location") else [])
        entities["query_type"] = parsed.get("query_type") or "general"
        entities["scheme_name"] = parsed.get("scheme_name") or ""

        if intent == "market":
            message = handle_market(query, data.get("markets", []), entities)
        elif intent == "scheme":
            message = handle_scheme(query, data.get("schemes", []))
        elif intent == "document":
            message = handle_document(query, data.get("documents", []))
        elif intent == "contact":
            message = handle_contact(query, data.get("contacts", []), entities)
        elif intent == "mandi":
            message = handle_mandi(query, data.get("mandis", []), entities)
        else:
            message = FALLBACK_MESSAGE

        return {
            "status": "success",
            "intent": intent,
            "data": message or FALLBACK_MESSAGE,
            "response": message or FALLBACK_MESSAGE,
        }
    except Exception:
        logger.exception("chat service failed")
        return {
            "status": "error",
            "message": "Something went wrong",
        }
