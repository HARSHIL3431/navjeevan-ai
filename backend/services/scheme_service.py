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


def handle_scheme(query: str, schemes: List[Dict[str, Any]]) -> str:
    try:
        if not schemes:
            return FALLBACK_MESSAGE

        q = (query or "").lower()
        match = None
        for scheme in schemes:
            keywords = scheme.get("keywords", [])
            if any(str(keyword).lower() in q for keyword in keywords):
                match = scheme
                break

        if match is None:
            match = _first_or_none(schemes)
        if not match:
            return FALLBACK_MESSAGE

        steps = match.get("steps", [])[:2]
        docs = match.get("documents", [])[:3]
        step_lines = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(steps)) or "1. Visit nearest CSC."
        doc_lines = "\n".join(f"- {doc}" for doc in docs) or "- Aadhaar card"

        return _finalize_response(
            "SCHEME:\n"
            f"Scheme: {match.get('scheme', 'N/A')}\n"
            f"Who can apply: {match.get('who_can_apply', 'N/A')}\n"
            f"Benefit: {match.get('benefit', 'N/A')}\n\n"
            "Steps:\n"
            f"{step_lines}\n\n"
            "Documents:\n"
            f"{doc_lines}"
        )
    except Exception:
        logger.exception("scheme service failed")
        return FALLBACK_MESSAGE
