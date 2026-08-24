from __future__ import annotations

from datetime import date
from typing import Any, Iterable

from .store import get_city, load_cities


def _text_values(item: dict[str, Any]) -> Iterable[str]:
    yield item["id"]
    yield from item["name"].values()
    yield from item.get("aliases", [])
    yield from item.get("categories", [])
    summary = item.get("summary", {})
    if isinstance(summary, dict):
        yield from summary.values()


def search_spots(
    keyword: str = "",
    *,
    city: str | None = None,
    province: str | None = None,
    category: str | None = None,
    month: int | None = None,
    free_only: bool = False,
    max_hours: float | None = None,
) -> list[dict[str, Any]]:
    needle = keyword.casefold().strip()
    matches: list[dict[str, Any]] = []
    for city_item in load_cities():
        if city and city.casefold() not in {
            city_item["id"].casefold(),
            city_item["name"]["zh"].casefold(),
            city_item["name"]["en"].casefold(),
        }:
            continue
        if province and province.casefold() not in {
            city_item["province"]["zh"].casefold(),
            city_item["province"]["en"].casefold(),
        }:
            continue
        for spot in city_item["spots"]:
            if needle and not any(needle in text.casefold() for text in _text_values(spot)):
                continue
            if category and category.casefold() not in {
                value.casefold() for value in spot.get("categories", [])
            }:
                continue
            if month and month not in spot.get("best_months", []):
                continue
            if free_only and spot.get("ticket", {}).get("price_cny") != 0:
                continue
            if max_hours is not None and spot["duration_hours"][0] > max_hours:
                continue
            matches.append(
                {
                    **spot,
                    "city": city_item["name"],
                    "province": city_item["province"],
                }
            )
    return matches


def plan_itinerary(city: str, days: int = 1, interests: list[str] | None = None) -> dict[str, Any]:
    city_item = get_city(city)
    if city_item is None:
        raise ValueError(f"Unknown city: {city}")
    if not 1 <= days <= 14:
        raise ValueError("days must be between 1 and 14")

    wanted = {value.casefold() for value in (interests or [])}

    def score(spot: dict[str, Any]) -> tuple[int, str]:
        overlap = wanted.intersection(value.casefold() for value in spot.get("categories", []))
        return (-len(overlap), spot["id"])

    ordered = sorted(city_item["spots"], key=score)
    day_plans = [{"day": index, "spots": [], "estimated_hours": 0.0} for index in range(1, days + 1)]
    for spot in ordered:
        duration = sum(spot["duration_hours"]) / 2
        candidates = [day for day in day_plans if day["estimated_hours"] + duration <= 8]
        target = min(candidates or day_plans, key=lambda day: day["estimated_hours"])
        target["spots"].append(
            {
                "id": spot["id"],
                "name": spot["name"],
                "neighborhood": spot["neighborhood"],
                "duration_hours": duration,
            }
        )
        target["estimated_hours"] += duration

    return {
        "city": city_item["name"],
        "days": day_plans,
        "planning_notes": [
            "This is a rule-based draft, not a live navigation result.",
            "Verify opening hours, reservations, transport, and weather before departure.",
            "Spots in the same neighborhood should be grouped manually as coverage grows.",
        ],
    }


def freshness_report(max_age_days: int = 365, today: date | None = None) -> dict[str, Any]:
    reference = today or date.today()
    stale: list[dict[str, Any]] = []
    total = 0
    for city in load_cities():
        for spot in city["spots"]:
            total += 1
            verified = spot.get("last_verified")
            age = (reference - date.fromisoformat(verified)).days if verified else None
            if age is None or age > max_age_days:
                stale.append(
                    {
                        "id": spot["id"],
                        "city": city["id"],
                        "last_verified": verified,
                        "age_days": age,
                        "reason": "unverified" if age is None else "stale",
                    }
                )
    return {"checked_on": reference.isoformat(), "max_age_days": max_age_days, "total": total, "stale": stale}

