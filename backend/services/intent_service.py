import re
import logging
from typing import Any, Dict, List, Tuple

from backend.services.ai_service import parse_query_with_groq

logger = logging.getLogger(__name__)

CROPS: List[str] = [
    "wheat",
    "cotton",
    "groundnut",
    "rice",
    "paddy",
    "sugarcane",
]

LOCATIONS: List[str] = [
    "surat",
    "navsari",
    "bardoli",
    "anand",
    "rajkot",
    "ahmedabad",
    "vadodara",
    "bhavnagar",
    "junagadh",
    "mehsana",
    "bharuch",
    "gujarat",
]

INTENT_RULES: List[Tuple[str, List[str]]] = [
    ("scheme", ["scheme", "yojana", "subsidy", "benefit", "eligibility", "fasal bima", "pm kisan"]),
    ("document", ["document", "documents", "docs", "paper", "papers", "checklist", "kcc"]),
    ("contact", ["trader", "buyer", "contact", "phone", "number", "dealer"]),
    ("mandi", ["mandi", "apmc", "nearest", "near", "timings"]),
    ("market", ["market", "sell", "price", "rate", "best option", "msp"]),
]

_HINDI_CROP_MAP = {
    "gehun": "wheat",
    "गेहूं": "wheat",
    "गेहूँ": "wheat",
    "kapas": "cotton",
    "कपास": "cotton",
    "chawal": "rice",
    "चावल": "rice",
    "dhan": "paddy",
    "धान": "paddy",
    "ganna": "sugarcane",
    "गन्ना": "sugarcane",
}


def detect_intent(query: str) -> str:
    q = (query or "").lower()
    for intent, keywords in INTENT_RULES:
        if any(keyword in q for keyword in keywords):
            return intent
    return "market"


def extract_entities(query: str) -> Dict[str, str]:
    q = (query or "").lower()
    crop = next((item for item in CROPS if item in q), "")
    location = next((item for item in LOCATIONS if item in q), "")
    return {"crop": crop, "location": location}


def _extract_locations(query: str) -> List[str]:
    q = (query or "").lower()
    found: List[tuple[int, str]] = []
    for location in LOCATIONS:
        match = re.search(rf"\b{re.escape(location)}\b", q)
        if match:
            found.append((match.start(), location))

    found.sort(key=lambda item: item[0])
    ordered: List[str] = []
    for _, location in found:
        if location not in ordered:
            ordered.append(location)
    return ordered


def _normalize(parsed: Dict[str, Any]) -> Dict[str, Any]:
    crop = str(parsed.get("crop") or "").strip().lower()
    location = str(parsed.get("location") or "").strip().lower()
    query_type = str(parsed.get("query_type") or "general").strip().lower()
    scheme_name = str(parsed.get("scheme_name") or "").strip()
    raw_locations = parsed.get("locations") or []

    if crop in _HINDI_CROP_MAP:
        crop = _HINDI_CROP_MAP[crop]
    if crop and crop not in CROPS:
        crop = ""

    if location and location not in LOCATIONS:
        location = ""

    locations: List[str] = []
    if isinstance(raw_locations, list):
        for value in raw_locations:
            token = str(value or "").strip().lower()
            if token in LOCATIONS and token not in locations:
                locations.append(token)

    if location and location not in locations:
        locations.insert(0, location)
    if not location and locations:
        location = locations[0]

    if query_type not in {"price", "mandi", "scheme", "general"}:
        query_type = "general"

    return {
        "crop": crop,
        "location": location,
        "locations": locations,
        "query_type": query_type,
        "scheme_name": scheme_name,
    }


def _heuristic_parse(query: str) -> Dict[str, Any]:
    q = (query or "").strip().lower()

    for source, target in _HINDI_CROP_MAP.items():
        q = q.replace(source, target)

    crop = next((item for item in CROPS if re.search(rf"\b{re.escape(item)}\b", q)), "")
    locations = _extract_locations(q)
    location = locations[0] if locations else ""

    if re.search(r"\b(price|prices|rate|rates|bhav|msp|भाव)\b", q):
        query_type = "price"
    elif re.search(r"\b(mandi|apmc|market yard|nearest mandi)\b", q):
        query_type = "mandi"
    elif re.search(r"\b(scheme|yojana|pm kisan|fasal bima|subsidy|eligibility)\b", q):
        query_type = "scheme"
    else:
        query_type = "general"

    scheme_name = ""
    if "pm kisan" in q:
        scheme_name = "PM-KISAN"
    elif "fasal bima" in q:
        scheme_name = "PM Fasal Bima Yojana"

    if query_type == "mandi" and "compare" in q and crop:
        query_type = "price"

    return {
        "crop": crop,
        "location": location,
        "locations": locations,
        "query_type": query_type,
        "scheme_name": scheme_name,
    }


def parse_query(query: str) -> Dict[str, Any]:
    try:
        groq_parsed = parse_query_with_groq(query)
        heuristic_parsed = _heuristic_parse(query)

        if not groq_parsed:
            return _normalize(heuristic_parsed)

        merged = dict(groq_parsed)
        if not merged.get("crop"):
            merged["crop"] = heuristic_parsed.get("crop", "")
        if not merged.get("location"):
            merged["location"] = heuristic_parsed.get("location", "")
        if not merged.get("locations"):
            merged["locations"] = heuristic_parsed.get("locations", [])

        groq_query_type = str(merged.get("query_type") or "").strip().lower()
        heuristic_query_type = str(heuristic_parsed.get("query_type") or "").strip().lower()
        if groq_query_type in {"", "general"} and heuristic_query_type != "general":
            merged["query_type"] = heuristic_query_type

        if not merged.get("scheme_name"):
            merged["scheme_name"] = heuristic_parsed.get("scheme_name", "")

        return _normalize(merged)
    except Exception:
        logger.exception("intent parsing failed")
        return _normalize(_heuristic_parse(query))
