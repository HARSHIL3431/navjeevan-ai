import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)
FALLBACK_MESSAGE = "Sorry, I don't have this info. Please contact your local Krishi office."


def _first_or_none(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return items[0] if items else {}


def _finalize_response(text: str) -> str:
    words = text.split()
    if len(words) <= 120:
        return text
    return " ".join(words[:120]).rstrip() + "..."


def handle_document(query: str, documents: List[Dict[str, Any]]) -> str:
    try:
        if not documents:
            return FALLBACK_MESSAGE

        q = (query or "").lower()
        match = None
        for item in documents:
            keywords = item.get("keywords", [])
            if any(str(keyword).lower() in q for keyword in keywords):
                match = item
                break

        if match is None:
            match = _first_or_none(documents)
        if not match:
            return FALLBACK_MESSAGE

        docs = match.get("documents", [])[:5]
        if not docs:
            return FALLBACK_MESSAGE

        doc_lines = "\n".join(f"- {doc}" for doc in docs)
        return _finalize_response(
            "DOCUMENTS:\n"
            f"For: {match.get('doc_type', 'General')}\n"
            f"{doc_lines}\n\n"
            f"Tip: {match.get('tip', 'Carry originals and photocopies.')}"
        )
    except Exception:
        logger.exception("document service failed")
        return FALLBACK_MESSAGE
