import json
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from pathlib import Path
from typing import Any, Dict

try:
    from groq import Groq
except Exception:
    Groq = None

from backend.config.settings import settings

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"


def _extract_json(text: str) -> Dict[str, Any]:
    if not text:
        return {}
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or start >= end:
        return {}
    try:
        payload = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _read_prompt(name: str, fallback: str) -> str:
    path = PROMPTS_DIR / name
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8").strip() or fallback


def parse_query_with_groq(query: str) -> Dict[str, Any]:
    api_key = settings.groq_api_key.strip()
    if not api_key or Groq is None:
        return {}

    client = Groq(api_key=api_key)
    model = settings.groq_model
    system_prompt = _read_prompt(
        "intent.txt",
        "Extract crop, location, locations, query_type, scheme_name from farmer query. Return JSON only.",
    )

    try:
        def _run() -> Any:
            return client.chat.completions.create(
                model=model,
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: {query}"},
                ],
            )

        with ThreadPoolExecutor(max_workers=1) as executor:
            response = executor.submit(_run).result(timeout=settings.groq_timeout_seconds)
        content = response.choices[0].message.content if response.choices else ""
        return _extract_json(content)
    except FuturesTimeoutError:
        logger.warning("Groq parse timed out")
        return {}
    except Exception:
        logger.exception("Groq parse failed")
        return {}


def format_response_with_groq(query: str, raw_response: str) -> str:
    api_key = settings.groq_api_key.strip()
    if not api_key or Groq is None:
        return raw_response

    client = Groq(api_key=api_key)
    model = settings.groq_model
    system_prompt = _read_prompt(
        "response.txt",
        "Rewrite answers in simple farmer-friendly English. Keep facts and numbers unchanged.",
    )

    try:
        def _run() -> Any:
            return client.chat.completions.create(
                model=model,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: {query}\nAnswer: {raw_response}"},
                ],
            )

        with ThreadPoolExecutor(max_workers=1) as executor:
            response = executor.submit(_run).result(timeout=settings.groq_timeout_seconds)
        text = response.choices[0].message.content if response.choices else ""
        return text.strip() or raw_response
    except FuturesTimeoutError:
        logger.warning("Groq format timed out")
        return raw_response
    except Exception:
        logger.exception("Groq format failed")
        return raw_response
