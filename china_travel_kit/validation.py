from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from .store import DATA_DIR


REQUIRED_CITY_KEYS = {
    "schema_version", "id", "name", "province", "overview", "weather", "tourism_portals", "transport", "stay_areas",
    "seasonal_advice", "culture", "foods", "emergency", "sources", "spots",
}
REQUIRED_SPOT_KEYS = {
    "id", "name", "categories", "neighborhood", "area_id", "neighborhood_name", "location", "duration_hours",
    "best_months", "ticket", "booking", "summary", "warnings", "sources", "last_verified",
}


def validate_city(city: dict[str, Any], filename: str = "<memory>") -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_CITY_KEYS - city.keys()
    if missing:
        errors.append(f"{filename}: missing city keys: {', '.join(sorted(missing))}")
        return errors
    if city["schema_version"] != 2:
        errors.append(f"{filename}: schema_version must be 2")
    if not city["spots"]:
        errors.append(f"{filename}: spots must not be empty")
    weather = city["weather"]
    if not all(str(weather.get(field, "")).startswith(("https://", "http://")) for field in ("forecast_url", "warnings_url")):
        errors.append(f"{filename}: weather forecast_url and warnings_url must be HTTP URLs")
    if not all(weather.get("provider", {}).get(language) and weather.get("note", {}).get(language) for language in ("zh", "en")):
        errors.append(f"{filename}: weather provider and note must be bilingual")
    try:
        date.fromisoformat(weather["last_verified"])
    except (KeyError, TypeError, ValueError):
        errors.append(f"{filename}: weather last_verified must be YYYY-MM-DD")
    if not city["tourism_portals"]:
        errors.append(f"{filename}: tourism_portals must not be empty")
    for index, portal in enumerate(city["tourism_portals"]):
        label = f"{filename}: tourism_portals[{index}]"
        if not {"name", "url", "operator", "use_for", "last_verified"} <= portal.keys():
            errors.append(f"{label}: missing sourced tourism portal fields")
            continue
        if not str(portal["url"]).startswith(("https://", "http://")):
            errors.append(f"{label}: url must be an HTTP URL")
        if not all(portal[field].get(language) for field in ("name", "operator", "use_for") for language in ("zh", "en")):
            errors.append(f"{label}: name, operator, and use_for must be bilingual")
        try:
            date.fromisoformat(portal["last_verified"])
        except (TypeError, ValueError):
            errors.append(f"{label}: last_verified must be YYYY-MM-DD")
    for field in ("international_gateways", "local", "notes"):
        for index, value in enumerate(city["transport"].get(field, [])):
            if not isinstance(value, dict) or not all(value.get(language) for language in ("zh", "en")):
                errors.append(f"{filename}: transport.{field}[{index}] must be bilingual")
    for index, area in enumerate(city["stay_areas"]):
        label = f"{filename}: stay_areas[{index}]"
        if not {"id", "name", "tradeoff"} <= area.keys():
            errors.append(f"{label}: id, name, and tradeoff are required")
        elif not all(area["name"].get(language) and area["tradeoff"].get(language) for language in ("zh", "en")):
            errors.append(f"{label}: name and tradeoff must be bilingual")
    for index, item in enumerate(city["seasonal_advice"]):
        label = f"{filename}: seasonal_advice[{index}]"
        if not {"months", "clothing", "gear", "risks"} <= item.keys():
            errors.append(f"{label}: months, clothing, gear, and risks are required")
            continue
        if any(not 1 <= month <= 12 for month in item["months"]):
            errors.append(f"{label}: months must contain values from 1 to 12")
        if not all(item["clothing"].get(language) for language in ("zh", "en")):
            errors.append(f"{label}: clothing must be bilingual")
    for index, service in enumerate(city["emergency"]):
        label = f"{filename}: emergency[{index}]"
        required = {"service", "phone", "scope", "source", "last_verified"}
        if not required <= service.keys():
            errors.append(f"{label}: missing sourced emergency fields")
            continue
        if not all(service["service"].get(language) for language in ("zh", "en")):
            errors.append(f"{label}: service must be bilingual")
        try:
            date.fromisoformat(service["last_verified"])
        except ValueError:
            errors.append(f"{label}: last_verified must be YYYY-MM-DD")
    for index, food in enumerate(city["foods"]):
        label = f"{filename}: foods[{index}]"
        if not all(food.get("name", {}).get(language) for language in ("zh", "en")):
            errors.append(f"{label}: name must be bilingual")
        for note_index, note in enumerate(food.get("dietary_notes", [])):
            if not isinstance(note, dict) or not all(note.get(language) for language in ("zh", "en")):
                errors.append(f"{label}: dietary_notes[{note_index}] must be bilingual")
    seen: set[str] = set()
    for index, spot in enumerate(city["spots"]):
        label = f"{filename}: spots[{index}]"
        missing_spot = REQUIRED_SPOT_KEYS - spot.keys()
        if missing_spot:
            errors.append(f"{label}: missing keys: {', '.join(sorted(missing_spot))}")
            continue
        if spot["id"] in seen:
            errors.append(f"{label}: duplicate id {spot['id']}")
        seen.add(spot["id"])
        if not spot.get("area_id") or not spot.get("neighborhood_name"):
            errors.append(f"{label}: area_id and neighborhood_name are required")
        availability = spot.get("availability")
        if availability:
            if availability.get("status") not in {"open", "temporarily-closed", "unknown"}:
                errors.append(f"{label}: invalid availability status")
            if not all(availability.get("note", {}).get(language) for language in ("zh", "en")):
                errors.append(f"{label}: availability note must be bilingual")
            try:
                date.fromisoformat(availability["as_of"])
            except (KeyError, TypeError, ValueError):
                errors.append(f"{label}: availability as_of must be YYYY-MM-DD")
        rating = spot.get("tourism_rating")
        if rating:
            if rating.get("level") not in {"5A", "4A"}:
                errors.append(f"{label}: tourism_rating level must be 5A or 4A")
            if not str(rating.get("source", "")).startswith(("https://", "http://")):
                errors.append(f"{label}: tourism_rating source must be an HTTP URL")
            if not all(rating.get("scope_note", {}).get(language) for language in ("zh", "en")):
                errors.append(f"{label}: tourism_rating scope_note must be bilingual")
            try:
                date.fromisoformat(rating["last_verified"])
            except (KeyError, TypeError, ValueError):
                errors.append(f"{label}: tourism_rating last_verified must be YYYY-MM-DD")
        if len(spot["duration_hours"]) != 2 or spot["duration_hours"][0] > spot["duration_hours"][1]:
            errors.append(f"{label}: duration_hours must be [minimum, maximum]")
        if any(not 1 <= month <= 12 for month in spot["best_months"]):
            errors.append(f"{label}: best_months must contain values from 1 to 12")
        if not spot["sources"]:
            errors.append(f"{label}: at least one source is required")
        if spot["last_verified"]:
            try:
                date.fromisoformat(spot["last_verified"])
            except ValueError:
                errors.append(f"{label}: last_verified must be YYYY-MM-DD or null")
    return errors


def validate_repository(data_dir: Path = DATA_DIR) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    paths = sorted(data_dir.glob("*.json"))
    if not paths:
        return [f"No JSON data found in {data_dir}"]
    for path in paths:
        try:
            city = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: invalid JSON: {exc}")
            continue
        errors.extend(validate_city(city, path.name))
        if city.get("id") in ids:
            errors.append(f"{path.name}: duplicate city id {city['id']}")
        ids.add(city.get("id"))
    return errors
