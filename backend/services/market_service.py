import logging
from typing import Any, Dict, List

from backend.services.ai_service import format_response_with_groq
from backend.utils.realtime_api import fetch_realtime_market_price

logger = logging.getLogger(__name__)
FALLBACK_MESSAGE = "Sorry, I don't have this info. Please contact your local Krishi office."


def _first_or_none(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return items[0] if items else {}


def _finalize_response(text: str) -> str:
    words = text.split()
    if len(words) <= 120:
        return text
    return " ".join(words[:120]).rstrip() + "..."


def _extract_price_per_qtl(item: Dict[str, Any], crop: str) -> Any:
    crop = (crop or "").strip().lower()
    if not crop:
        return None

    # Flat structure support: price_per_qtl = {"wheat": 2100}
    flat = item.get("price_per_qtl", {})
    if isinstance(flat, dict):
        value = flat.get(crop)
        if isinstance(value, (int, float)):
            return value

    # Nested structure support: crops = {"wheat": {"price_per_qtl": 2100}}
    nested_crops = item.get("crops", {})
    if isinstance(nested_crops, dict):
        crop_meta = nested_crops.get(crop, {})
        if isinstance(crop_meta, dict):
            value = crop_meta.get("price_per_qtl")
            if isinstance(value, (int, float)):
                return value
        if isinstance(crop_meta, (int, float)):
            return crop_meta

    return None


def _crop_exists(item: Dict[str, Any], crop: str) -> bool:
    crop = (crop or "").strip().lower()
    crops = item.get("crops", [])
    if isinstance(crops, list):
        return crop in [str(value).strip().lower() for value in crops]
    if isinstance(crops, dict):
        return crop in [str(key).strip().lower() for key in crops.keys()]
    return False


def _filter_markets(markets: List[Dict[str, Any]], crop: str, location: str) -> List[Dict[str, Any]]:
    crop = (crop or "").strip().lower()
    location = (location or "").strip().lower()

    if not crop or not location:
        return []

    exact_city_matches: List[Dict[str, Any]] = []
    partial_city_matches: List[Dict[str, Any]] = []

    for item in markets:
        city = str(item.get("city", "")).strip().lower()
        if not _crop_exists(item, crop):
            continue

        if city == location:
            exact_city_matches.append(item)
        elif location in city:
            partial_city_matches.append(item)

    return exact_city_matches or partial_city_matches


def _nearest_crop_markets(markets: List[Dict[str, Any]], crop: str, limit: int = 3) -> List[Dict[str, Any]]:
    crop = (crop or "").strip().lower()
    if not crop:
        return []

    crop_matches = [item for item in markets if _crop_exists(item, crop)]

    def _distance(value: Dict[str, Any]) -> float:
        try:
            return float(value.get("distance_km", 10**9))
        except (TypeError, ValueError):
            return float(10**9)

    return sorted(crop_matches, key=_distance)[: max(limit, 1)]


def _resolve_market_for_location(markets: List[Dict[str, Any]], crop: str, location: str, query_type: str) -> Dict[str, Any]:
    location = (location or "").strip().lower()
    if not location:
        return {}

    if query_type == "price":
        live_data = fetch_realtime_market_price(crop, location)
        if live_data:
            local_match = _first_or_none(_filter_markets(markets, crop, location))
            return {
                "market": live_data.get("market_name", "N/A"),
                "location": str(live_data.get("location", location)),
                "price": live_data.get("price_per_qtl"),
                "contact": (
                    f"{local_match.get('contact_person', 'N/A')} - {local_match.get('phone', 'N/A')}"
                    if local_match
                    else "N/A"
                ),
                "tip": (
                    local_match.get("tip", "Live market data fetched successfully.")
                    if local_match
                    else "Live market data fetched successfully."
                ),
                "source": str(live_data.get("source", "Live API")),
            }

    candidates = _filter_markets(markets, crop, location)
    target = _first_or_none(candidates)
    if not target:
        return {}

    price = _extract_price_per_qtl(target, crop)
    if price is None:
        return {}

    return {
        "market": target.get("name", "N/A"),
        "location": target.get("city", location.title()),
        "price": price,
        "contact": f"{target.get('contact_person', 'N/A')} - {target.get('phone', 'N/A')}",
        "tip": target.get("tip", "Visit early morning for better rates."),
        "source": "Dataset",
    }


def handle_market(query: str, markets: List[Dict[str, Any]], entities: Dict[str, Any]) -> str:
    try:
        if not markets:
            return FALLBACK_MESSAGE

        crop = (entities.get("crop") or "").lower()
        location = (entities.get("location") or "").lower()
        query_type = (entities.get("query_type") or "general").lower()
        locations = entities.get("locations") or []

        if not isinstance(locations, list):
            locations = []

        normalized_locations = []
        for token in locations:
            value = str(token or "").strip().lower()
            if value and value not in normalized_locations:
                normalized_locations.append(value)

        if not crop:
            return FALLBACK_MESSAGE

        comparison_requested = "compare" in (query or "").lower() or len(normalized_locations) >= 2
        if comparison_requested and normalized_locations:
            comparison_rows = []
            missing_locations = []
            for loc in normalized_locations:
                result = _resolve_market_for_location(markets, crop, loc, query_type)
                if result:
                    comparison_rows.append(result)
                else:
                    missing_locations.append(loc)

            if comparison_rows:
                rows_with_price = [row for row in comparison_rows if isinstance(row.get("price"), (int, float))]
                best = max(rows_with_price, key=lambda row: row["price"]) if rows_with_price else comparison_rows[0]

                lines = [f"COMPARISON ({crop.title()}):"]
                for row in comparison_rows:
                    lines.append(
                        f"- {str(row.get('location', 'N/A')).title()}: Rs. {row.get('price', 'N/A')}/qtl at "
                        f"{row.get('market', 'N/A')} ({row.get('source', 'Dataset')})"
                    )

                lines.append(
                    f"Best option: {best.get('market', 'N/A')} in {str(best.get('location', 'N/A')).title()} "
                    f"at Rs. {best.get('price', 'N/A')}/qtl"
                )

                if missing_locations:
                    lines.append("Data not available for: " + ", ".join(city.title() for city in missing_locations))

                lines.append(f"Contact: {best.get('contact', 'N/A')}")
                lines.append(f"Tip: {best.get('tip', 'Visit early morning for better rates.')}")
                return _finalize_response("\n".join(lines))

        if query_type == "price" and location:
            live_or_dataset = _resolve_market_for_location(markets, crop, location, query_type)
            if live_or_dataset:
                response_text = _finalize_response(
                    f"Best option: {live_or_dataset.get('market', 'N/A')}, {live_or_dataset.get('location', 'N/A')}\n"
                    f"Price: Rs. {live_or_dataset.get('price', 'N/A')}/qtl\n"
                    f"Contact: {live_or_dataset.get('contact', 'N/A')}\n"
                    f"Source: {live_or_dataset.get('source', 'Dataset')}\n\n"
                    f"Tip: {live_or_dataset.get('tip', 'Visit early morning for better rates.')}"
                )
                return format_response_with_groq(query, response_text)

        candidates = _filter_markets(markets, crop, location)
        used_fallback = False
        if not candidates:
            candidates = _nearest_crop_markets(markets, crop, limit=3)
            used_fallback = True

        target = _first_or_none(candidates)
        if not target:
            return FALLBACK_MESSAGE

        price = _extract_price_per_qtl(target, crop)
        if price is None:
            return FALLBACK_MESSAGE

        response = (
            f"Best option: {target.get('name', 'N/A')}, {target.get('city', 'N/A')}\n"
            f"Price: Rs. {price}/qtl\n"
            f"Distance: {target.get('distance_km', 'N/A')} km\n"
            f"Contact: {target.get('contact_person', 'N/A')} - {target.get('phone', 'N/A')}\n\n"
            f"Tip: {target.get('tip', 'Visit early morning for better rates.')}"
        )

        if used_fallback and location:
            response = f"Location '{location.title()}' not found. Showing nearest {crop.title()} markets.\n" + response

        return format_response_with_groq(query, _finalize_response(response))
    except Exception:
        logger.exception("market service failed")
        return FALLBACK_MESSAGE
