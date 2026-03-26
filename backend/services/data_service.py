import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

_BASE_DIR = Path(__file__).resolve().parents[1]
_DATA_DIR = _BASE_DIR / "data"

_store: Dict[str, List[Dict[str, Any]]] = {
    "markets": [],
    "schemes": [],
    "documents": [],
    "contacts": [],
    "mandis": [],
}
_loaded = False


def _load_file(file_name: str) -> List[Dict[str, Any]]:
    path = _DATA_DIR / file_name
    with path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    return payload if isinstance(payload, list) else []


def load_data() -> None:
    global _loaded
    try:
        _store["markets"] = _load_file("markets.json")
        _store["schemes"] = _load_file("schemes.json")
        _store["documents"] = _load_file("documents.json")
        _store["contacts"] = _load_file("contacts.json")
        _store["mandis"] = _load_file("mandis.json")
        _loaded = True
        logger.info("Dataset cache initialized")
    except Exception:
        logger.exception("Failed to load datasets")
        _loaded = False


def ensure_data_loaded() -> None:
    if not _loaded:
        load_data()


def get_all_data() -> Dict[str, List[Dict[str, Any]]]:
    return _store
