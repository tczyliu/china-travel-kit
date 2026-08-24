from __future__ import annotations

import json
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent


def resolve_data_dir() -> Path:
    override = os.environ.get("CHINA_TRAVEL_KIT_DATA")
    candidates = [
        Path(override).expanduser() if override else None,
        ROOT / "data" / "cities",
        Path(sys.prefix) / "share" / "china-travel-kit" / "data" / "cities",
    ]
    for candidate in candidates:
        if candidate and candidate.is_dir():
            return candidate
    attempted = ", ".join(str(path) for path in candidates if path)
    raise DataError(f"Cannot find city data. Tried: {attempted}")


class DataError(RuntimeError):
    """Raised when repository data cannot be loaded safely."""


def resolve_web_dir() -> Path:
    override = os.environ.get("CHINA_TRAVEL_KIT_WEB")
    candidates = [
        Path(override).expanduser() if override else None,
        ROOT / "web",
        Path(sys.prefix) / "share" / "china-travel-kit" / "web",
    ]
    for candidate in candidates:
        if candidate and candidate.is_dir():
            return candidate
    attempted = ", ".join(str(path) for path in candidates if path)
    raise DataError(f"Cannot find web assets. Tried: {attempted}")


DATA_DIR = resolve_data_dir()
WEB_DIR = resolve_web_dir()


@lru_cache(maxsize=1)
def load_cities() -> tuple[dict[str, Any], ...]:
    cities: list[dict[str, Any]] = []
    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            city = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise DataError(f"Cannot load {path}: {exc}") from exc
        city["_file"] = path.name
        cities.append(city)
    if not cities:
        raise DataError(f"No city data found in {DATA_DIR}")
    return tuple(cities)


def get_city(value: str) -> dict[str, Any] | None:
    needle = value.casefold().strip()
    for city in load_cities():
        names = city["name"]
        candidates = {city["id"], names["zh"], names["en"], names.get("pinyin", "")}
        if needle in {candidate.casefold() for candidate in candidates}:
            return city
    return None
