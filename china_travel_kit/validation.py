from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from .store import DATA_DIR


REQUIRED_CITY_KEYS = {"schema_version", "id", "name", "province", "overview", "sources", "spots"}
REQUIRED_SPOT_KEYS = {
    "id", "name", "categories", "neighborhood", "location", "duration_hours",
    "best_months", "ticket", "booking", "summary", "warnings", "sources", "last_verified",
}


def validate_city(city: dict[str, Any], filename: str = "<memory>") -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_CITY_KEYS - city.keys()
    if missing:
        errors.append(f"{filename}: missing city keys: {', '.join(sorted(missing))}")
        return errors
    if city["schema_version"] != 1:
        errors.append(f"{filename}: schema_version must be 1")
    if not city["spots"]:
        errors.append(f"{filename}: spots must not be empty")
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

