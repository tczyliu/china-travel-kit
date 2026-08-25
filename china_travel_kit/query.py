from __future__ import annotations

from datetime import date
from math import asin, cos, radians, sin, sqrt
from typing import Any, Iterable

from .store import get_city, load_cities


PACE_HOURS = {"relaxed": 4.0, "balanced": 6.0, "full": 8.0}
MOBILITY_WARNING_MARKERS = {
    "long walking distances",
    "large site",
    "uneven and slippery stone lanes",
    "slippery paths after rain",
    "high altitude",
    "altitude",
}
INTEREST_KEYWORDS = {
    "wildlife": ("熊猫", "动物", "wildlife", "panda"),
    "food": ("美食", "小吃", "火锅", "餐饮", "food", "cuisine"),
    "history": ("历史", "古城", "故宫", "三国", "history", "historic"),
    "museum": ("博物馆", "博物院", "museum"),
    "architecture": ("建筑", "architecture"),
    "photography": ("摄影", "拍照", "出片", "photography", "photo"),
    "nature": ("自然", "山水", "风景", "nature", "scenery"),
    "mountain": ("爬山", "雪山", "山野", "mountain", "hiking"),
    "family": ("亲子", "孩子", "儿童", "family", "children", "kids"),
    "shopping": ("购物", "逛街", "shopping"),
    "local-life": ("本地生活", "社区", "local life", "neighborhood"),
    "nightlife": ("夜游", "夜生活", "nightlife"),
    "culture": ("文化", "民俗", "民族", "culture", "heritage"),
}


def _text_values(item: dict[str, Any]) -> Iterable[str]:
    yield item["id"]
    yield from item["name"].values()
    yield from item.get("aliases", [])
    yield from item.get("categories", [])
    summary = item.get("summary", {})
    if isinstance(summary, dict):
        yield from summary.values()


def _localized_values(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            if isinstance(item, str):
                yield item


def _matches_city(city_item: dict[str, Any], city: str | None, province: str | None) -> bool:
    if city and city.casefold() not in {
        city_item["id"].casefold(),
        city_item["name"]["zh"].casefold(),
        city_item["name"]["en"].casefold(),
    }:
        return False
    if province and province.casefold() not in {
        city_item["province"]["zh"].casefold(),
        city_item["province"]["en"].casefold(),
    }:
        return False
    return True


def _spot_texts(spot: dict[str, Any]) -> list[str]:
    return [text.casefold() for text in _text_values(spot) if isinstance(text, str)]


def _spot_matches_terms(spot: dict[str, Any], terms: Iterable[str]) -> bool:
    texts = _spot_texts(spot)
    return any(term.casefold().strip() in text for term in terms if term.strip() for text in texts)


def _has_mobility_caution(spot: dict[str, Any]) -> bool:
    warnings = {warning.casefold() for warning in spot.get("warnings", [])}
    return bool(warnings.intersection(MOBILITY_WARNING_MARKERS))


def _distance_km(left: dict[str, Any], right: dict[str, Any]) -> float | None:
    if not all(key in left and key in right for key in ("lat", "lng")):
        return None
    lat1, lng1, lat2, lng2 = map(radians, (left["lat"], left["lng"], right["lat"], right["lng"]))
    delta_lat = lat2 - lat1
    delta_lng = lng2 - lng1
    value = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lng / 2) ** 2
    return round(6371 * 2 * asin(sqrt(value)), 1)


def _cultural_context(city_item: dict[str, Any], spot: dict[str, Any]) -> dict[str, str]:
    if spot.get("cultural_context"):
        return spot["cultural_context"]
    themes = city_item.get("culture", [])[:2]
    zh_themes = "、".join(item["zh"] for item in themes)
    en_themes = " and ".join(item["en"] for item in themes)
    categories = set(spot.get("categories", []))
    if categories.intersection({"history", "museum", "archaeology", "architecture", "world-heritage"}):
        zh_focus = "游览时可留意空间格局、历史层次和展陈如何讲述当地社会"
        en_focus = "Look for how spatial design, historical layers, and interpretation explain local society"
    elif categories.intersection({"local-life", "food", "walking", "nightlife"}):
        zh_focus = "这里也是当代社区生活的一部分，请在体验商业与饮食之外尊重居民日常"
        en_focus = "This is also part of contemporary neighborhood life; enjoy food and commerce while respecting residents"
    else:
        zh_focus = "可同时观察自然环境、公共空间与城市生活之间的关系"
        en_focus = "Notice the relationship between the natural setting, public space, and urban life"
    return {
        "zh": f"{spot['summary']['zh']} {zh_focus}；可结合{zh_themes}理解这个地点。",
        "en": f"{spot['summary']['en']} {en_focus}; connect the visit with {en_themes}.",
    }


def _amenities_guidance(spot: dict[str, Any]) -> list[dict[str, Any]]:
    large_site = any(value in {"Large site", "Long walking distances"} for value in spot.get("warnings", []))
    return [
        {
            "code": "arrival_return",
            "label": {"zh": "到达与返程点", "en": "Arrival and return point"},
            "guidance": {
                "zh": "先确认实际入口、出口和返程上车点；大型景区不同入口可能相距较远。" if large_site else "先确认实际入口、出口和返程上车点，不要只按景点名称导航。",
                "en": "Confirm the actual entrance, exit, and return pickup point; entrances can be far apart at large sites." if large_site else "Confirm the actual entrance, exit, and return pickup point rather than navigating only by the attraction name.",
            },
        },
        {
            "code": "food_water",
            "label": {"zh": "餐饮与饮水", "en": "Food and water"},
            "guidance": {"zh": "景区内外餐饮条件可能不同，入场前查看官方导览并准备饮水。", "en": "Food options may differ inside and outside the site; check the official visitor map and carry water."},
        },
        {
            "code": "toilet_accessibility",
            "label": {"zh": "卫生间与无障碍", "en": "Toilets and accessibility"},
            "guidance": {"zh": "到达后优先确认游客中心、卫生间和无障碍路线，具体开放状态以现场为准。", "en": "On arrival, locate the visitor center, toilets, and accessible route; same-day availability must be checked onsite."},
        },
        {
            "code": "luggage",
            "label": {"zh": "行李寄存", "en": "Luggage storage"},
            "guidance": {"zh": "不要默认景点提供行李寄存；携带大件行李前先查官方说明。", "en": "Do not assume luggage storage is available; check official guidance before arriving with large bags."},
        },
    ]


def _nearby_spots(city_item: dict[str, Any], spot: dict[str, Any], limit: int = 3) -> list[dict[str, Any]]:
    nearby: list[tuple[float, dict[str, Any]]] = []
    for candidate in city_item["spots"]:
        if candidate["id"] == spot["id"] or candidate.get("availability", {}).get("status") == "temporarily-closed":
            continue
        distance = _distance_km(spot.get("location", {}), candidate.get("location", {}))
        if distance is not None:
            nearby.append((distance, candidate))
    return [
        {
            "id": candidate["id"],
            "name": candidate["name"],
            "neighborhood": candidate.get("neighborhood_name", {"zh": candidate["neighborhood"], "en": candidate["neighborhood"]}),
            "approx_distance_km": distance,
            "note": {"zh": "直线距离仅用于判断片区关系，实际路线与耗时需实时查询。", "en": "Straight-line distance is only for area planning; check the live route and travel time."},
        }
        for distance, candidate in sorted(nearby, key=lambda item: (item[0], item[1]["id"]))[:limit]
    ]


def _transfer_guidance(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    distance = _distance_km(left.get("location", {}), right.get("location", {}))
    same_area = left.get("area_id") == right.get("area_id")
    if same_area or (distance is not None and distance <= 2.5):
        guidance = {"zh": "优先步行或短途公共交通；出发前用地图核验实际入口和步行条件。", "en": "Prefer walking or a short public-transport hop; verify entrances and walking conditions in a live map."}
    elif distance is not None and distance <= 15:
        guidance = {"zh": "优先查询地铁或公交组合，携带儿童、行李或体力有限时再比较出租车/网约车。", "en": "Check metro or bus combinations first; compare taxi or ride-hailing when travelling with children, luggage, or limited mobility."}
    else:
        guidance = {"zh": "属于跨片区移动，预留换乘缓冲并核验末班车、交通管制和正规上车点。", "en": "This is a cross-area transfer; allow a buffer and verify last services, traffic controls, and legitimate pickup points."}
    return {
        "from": left["name"],
        "to": right["name"],
        "approx_distance_km": distance,
        "guidance": guidance,
        "live_check_required": True,
    }


def _infer_interests(requirements: str) -> set[str]:
    text = requirements.casefold()
    return {
        interest
        for interest, keywords in INTEREST_KEYWORDS.items()
        if any(keyword.casefold() in text for keyword in keywords)
    }


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
        if not _matches_city(city_item, city, province):
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
                    "tourism_portals": city_item["tourism_portals"],
                }
            )
    return matches


def discover_areas(
    keyword: str = "",
    *,
    city: str | None = None,
    province: str | None = None,
) -> list[dict[str, Any]]:
    """Find visitor-relevant stay areas and attraction neighborhoods."""
    needle = keyword.casefold().strip()
    matches: list[dict[str, Any]] = []
    for city_item in load_cities():
        if not _matches_city(city_item, city, province):
            continue

        spot_counts: dict[str, int] = {}
        spot_names: dict[str, dict[str, str]] = {}
        for spot in city_item["spots"]:
            area_id = spot.get("area_id", spot["neighborhood"].casefold().replace(" ", "-"))
            spot_counts[area_id] = spot_counts.get(area_id, 0) + 1
            spot_names[area_id] = spot.get(
                "neighborhood_name",
                {"zh": spot["neighborhood"], "en": spot["neighborhood"]},
            )

        seen: set[str] = set()
        for area in city_item.get("stay_areas", []):
            area_id = area["id"]
            seen.add(area_id)
            record = {
                "id": area_id,
                "kind": "stay-area",
                "name": area["name"],
                "tradeoff": area["tradeoff"],
                "indexed_spot_count": spot_counts.get(area_id, 0),
                "coverage_note": {
                    "zh": "数量仅表示当前开放数据集已收录的地点，不代表该区域全部景点。",
                    "en": "The count covers only places indexed in this open dataset, not every attraction in the area.",
                },
                "city": city_item["name"],
                "province": city_item["province"],
                "tourism_portals": city_item["tourism_portals"],
            }
            texts = [*_localized_values(area["name"]), *_localized_values(area["tradeoff"])]
            if not needle or any(needle in text.casefold() for text in texts):
                matches.append(record)

        for area_id, count in spot_counts.items():
            if area_id in seen:
                continue
            name = spot_names[area_id]
            if needle and not any(needle in text.casefold() for text in _localized_values(name)):
                continue
            matches.append(
                {
                    "id": area_id,
                    "kind": "attraction-area",
                    "name": name,
                    "tradeoff": None,
                    "indexed_spot_count": count,
                    "coverage_note": {
                        "zh": "数量仅表示当前开放数据集已收录的地点，不代表该区域全部景点。",
                        "en": "The count covers only places indexed in this open dataset, not every attraction in the area.",
                    },
                    "city": city_item["name"],
                    "province": city_item["province"],
                    "tourism_portals": city_item["tourism_portals"],
                }
            )
    return matches


def get_trip_preparation(city: str, month: int) -> dict[str, Any]:
    city_item = get_city(city)
    if city_item is None:
        raise ValueError(f"Unknown city: {city}")
    if not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")
    seasonal = [item for item in city_item.get("seasonal_advice", []) if month in item["months"]]
    return {
        "city": city_item["name"],
        "month": month,
        "seasonal_advice": seasonal,
        "weather": city_item.get("weather", {}),
        "tourism_portals": city_item.get("tourism_portals", []),
        "stay_areas": city_item.get("stay_areas", []),
        "transport": city_item.get("transport", {}),
        "culture": city_item.get("culture", []),
        "foods": city_item.get("foods", []),
        "limitations": {
            "zh": "这是季节性准备建议，不是实时天气、医疗建议或预订信息。出发前请核验天气预警和运营信息。",
            "en": "This is seasonal preparation guidance, not live weather, medical advice, or booking information. Verify alerts and operations before departure.",
        },
        "sources": city_item["sources"],
    }


def get_emergency_help(city: str) -> dict[str, Any]:
    city_item = get_city(city)
    if city_item is None:
        raise ValueError(f"Unknown city: {city}")
    return {
        "city": city_item["name"],
        "services": city_item.get("emergency", []),
        "instructions": {
            "zh": "如有危险，先移动到安全地点并清楚说明所在城市、附近地标和发生的事情。非紧急咨询不要占用紧急热线。",
            "en": "If in danger, move to a safe place first and clearly state the city, nearby landmark, and what happened. Do not use emergency lines for non-emergencies.",
        },
        "limitations": {
            "zh": "语言支持和接通方式可能因地区变化；离线保存的信息也应在出发前再次核验。",
            "en": "Language support and call handling may vary by locality; recheck saved offline information before travel.",
        },
    }


def plan_itinerary(
    city: str,
    days: int = 1,
    interests: list[str] | None = None,
    *,
    month: int | None = None,
    must_see: list[str] | None = None,
    pace: str = "full",
    mobility: str = "standard",
    free_only: bool = False,
) -> dict[str, Any]:
    city_item = get_city(city)
    if city_item is None:
        raise ValueError(f"Unknown city: {city}")
    if not 1 <= days <= 14:
        raise ValueError("days must be between 1 and 14")
    if month is not None and not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")
    if pace not in PACE_HOURS:
        raise ValueError("pace must be relaxed, balanced, or full")
    if mobility not in {"standard", "reduced"}:
        raise ValueError("mobility must be standard or reduced")

    wanted = {value.casefold() for value in (interests or [])}
    wanted_places = [value for value in (must_see or []) if value.strip()]
    daily_limit = PACE_HOURS[pace]

    def is_requested(spot: dict[str, Any]) -> bool:
        return _spot_matches_terms(spot, wanted_places)

    def visit_duration(spot: dict[str, Any]) -> float:
        minimum, maximum = spot["duration_hours"]
        if pace == "relaxed" or is_requested(spot):
            return float(minimum)
        return (minimum + maximum) / 2

    def score(spot: dict[str, Any]) -> tuple[int, int, int, int, str]:
        overlap = wanted.intersection(value.casefold() for value in spot.get("categories", []))
        place_match = is_requested(spot)
        seasonal_match = month is not None and month in spot.get("best_months", [])
        mobility_penalty = mobility == "reduced" and _has_mobility_caution(spot)
        return (-int(place_match), -len(overlap), -int(seasonal_match), int(mobility_penalty), spot["id"])

    unavailable = [
        {"id": spot["id"], "name": spot["name"], "availability": spot["availability"]}
        for spot in city_item["spots"]
        if spot.get("availability", {}).get("status") == "temporarily-closed"
    ]
    available_spots = [
        spot for spot in city_item["spots"]
        if spot.get("availability", {}).get("status") != "temporarily-closed"
        and (not free_only or spot.get("ticket", {}).get("price_cny") == 0)
    ]
    ordered = sorted(available_spots, key=score)
    day_plans = [
        {"day": index, "spots": [], "estimated_hours": 0.0, "locations": []}
        for index in range(1, days + 1)
    ]

    def add_spot(day: dict[str, Any], spot: dict[str, Any]) -> None:
        duration = visit_duration(spot)
        day["spots"].append(
            {
                "id": spot["id"],
                "name": spot["name"],
                "area_id": spot.get("area_id"),
                "neighborhood": spot.get(
                    "neighborhood_name",
                    {"zh": spot["neighborhood"], "en": spot["neighborhood"]},
                ),
                "location": spot.get("location", {}),
                "duration_hours": duration,
                "duration_range_hours": spot["duration_hours"],
                "pace_exception": duration > daily_limit,
                "summary": spot["summary"],
                "cultural_context": _cultural_context(city_item, spot),
                "nearby_spots": _nearby_spots(city_item, spot),
                "amenities_guidance": _amenities_guidance(spot),
                "sources": spot.get("sources", []),
            }
        )
        day["estimated_hours"] += duration
        if "lat" in spot.get("location", {}) and "lng" in spot["location"]:
            day["locations"].append(spot["location"])

    remaining = ordered[:]
    for day in day_plans:
        seed = next(
            (spot for spot in remaining if visit_duration(spot) <= daily_limit or is_requested(spot)),
            None,
        )
        if seed is not None:
            remaining.remove(seed)
            add_spot(day, seed)

    for day in day_plans:
        while True:
            candidates = [
                spot for spot in remaining
                if day["estimated_hours"] + visit_duration(spot) <= daily_limit
            ]
            if not candidates:
                break

            def candidate_score(spot: dict[str, Any]) -> tuple[int, int, int, int, float, str]:
                location = spot.get("location", {})
                if not day["locations"] or "lat" not in location or "lng" not in location:
                    distance = float("inf")
                else:
                    distance = min(
                        (location["lat"] - item["lat"]) ** 2 + (location["lng"] - item["lng"]) ** 2
                        for item in day["locations"]
                    )
                return (*score(spot)[:-1], distance, spot["id"])

            selected = min(candidates, key=candidate_score)
            remaining.remove(selected)
            add_spot(day, selected)

    unassigned = [
        {
            "id": spot["id"],
            "name": spot["name"],
            "reason": {
                "code": "daily_time_limit",
                "zh": f"超过每日约 {daily_limit:g} 小时的活动上限。",
                "en": f"It would exceed the daily activity limit of about {daily_limit:g} hours.",
            },
        }
        for spot in remaining
    ]

    pace_exceptions: list[dict[str, Any]] = []
    for day in day_plans:
        exception_spot = next((spot for spot in day["spots"] if spot["pace_exception"]), None)
        if exception_spot is None:
            day["pace_exception"] = None
            continue
        note = {
            "zh": f"你明确指定了{exception_spot['name']['zh']}；其最短建议游览约 {exception_spot['duration_hours']:g} 小时，超过轻松节奏每天约 {daily_limit:g} 小时的偏好，因此单独安排一天。请结合体力、海拔和现场交通决定是否保留。",
            "en": f"You explicitly requested {exception_spot['name']['en']}. Its shortest suggested visit is about {exception_spot['duration_hours']:g} hours, above the preferred {daily_limit:g} hours/day, so it is scheduled alone. Keep it only after checking stamina, altitude, and local transport.",
        }
        day["pace_exception"] = note
        pace_exceptions.append(
            {
                "day": day["day"],
                "spot": exception_spot["name"],
                "estimated_hours": exception_spot["duration_hours"],
                "preferred_daily_hours": daily_limit,
                "note": note,
            }
        )

    planned_ids = {spot["id"] for day in day_plans for spot in day["spots"]}
    planned_area_counts: dict[str, int] = {}
    for day in day_plans:
        del day["locations"]
        day["transfers"] = [
            _transfer_guidance(left, right)
            for left, right in zip(day["spots"], day["spots"][1:])
        ]
        for spot in day["spots"]:
            if spot.get("area_id"):
                planned_area_counts[spot["area_id"]] = planned_area_counts.get(spot["area_id"], 0) + 1

    stay_areas = [
        {**area, "planned_spot_count": planned_area_counts.get(area["id"], 0)}
        for area in city_item.get("stay_areas", [])
    ]
    stay_area_order = {area["id"]: index for index, area in enumerate(city_item.get("stay_areas", []))}
    recommended_stay_areas = sorted(
        stay_areas,
        key=lambda area: (-area["planned_spot_count"], stay_area_order[area["id"]]),
    )[:2]
    transport_modes = "、".join(item["zh"] for item in city_item.get("transport", {}).get("local", [])[:3])
    transport_modes_en = ", ".join(item["en"] for item in city_item.get("transport", {}).get("local", [])[:3])
    base_area = recommended_stay_areas[0] if recommended_stay_areas else None
    for day in day_plans:
        if not day["spots"]:
            day["arrival_guidance"] = None
            continue
        first = day["spots"][0]
        same_base_area = base_area and base_area["id"] == first.get("area_id")
        if same_base_area:
            guidance = {
                "zh": f"从{base_area['name']['zh']}出发，优先步行或短途公共交通前往首站；仍需核验实际入口。",
                "en": f"From {base_area['name']['en']}, prefer walking or a short public-transport hop to the first stop; verify the actual entrance.",
            }
        else:
            guidance = {
                "zh": f"从建议住宿区域前往首站时，优先比较{transport_modes}；出发前用实时地图核验路线、换乘和运营时间。",
                "en": f"From the suggested stay area, compare {transport_modes_en}; verify the live route, transfers, and service hours before leaving.",
            }
        day["arrival_guidance"] = {
            "from_area": base_area["name"] if base_area else None,
            "to": first["name"],
            "guidance": guidance,
            "live_check_required": True,
        }

    caution_spots = [
        {"id": spot["id"], "name": spot["name"], "warnings": spot.get("warnings", [])}
        for spot in available_spots
        if mobility == "reduced"
        and _has_mobility_caution(spot)
        and (spot["id"] in planned_ids or _spot_matches_terms(spot, wanted_places))
    ]

    return {
        "city": city_item["name"],
        "days": day_plans,
        "daily_limit_hours": daily_limit,
        "unassigned_spots": unassigned,
        "unavailable_spots": unavailable,
        "caution_spots": caution_spots,
        "pace_exceptions": pace_exceptions,
        "recommended_stay_areas": recommended_stay_areas,
        "transport": city_item.get("transport", {}),
        "weather": city_item.get("weather", {}),
        "tourism_portals": city_item.get("tourism_portals", []),
        "planning_notes": [
            {
                "zh": "这是基于兴趣、区域和游览时长生成的规则草案，不是实时导航结果。",
                "en": "This is a rule-based draft using interests, areas, and visit duration, not a live navigation result.",
            },
            {
                "zh": "出发前请核验开放时间、预约、交通和天气。",
                "en": "Verify opening hours, reservations, transport, and weather before departure.",
            },
            {
                "zh": f"通常每天最多安排约 {daily_limit:g} 小时；明确指定但最短游览时间更长的地点会单独占用一天并醒目标注。",
                "en": f"Days are normally capped at about {daily_limit:g} activity hours; an explicitly requested place with a longer minimum visit is scheduled alone and clearly flagged.",
            },
        ],
    }


def recommend_trip(
    *,
    traveler_count: int = 1,
    start_date: str | None = None,
    end_date: str | None = None,
    month: int | None = None,
    days: int | None = None,
    city: str | None = None,
    desired_places: list[str] | None = None,
    interests: list[str] | None = None,
    pace: str = "balanced",
    budget: str = "moderate",
    mobility: str = "standard",
    children: bool = False,
    origin_country: str | None = None,
    requirements: str = "",
) -> dict[str, Any]:
    """Match traveler requirements to covered cities and return an explainable draft."""
    if not 1 <= traveler_count <= 20:
        raise ValueError("traveler_count must be between 1 and 20")
    if pace not in PACE_HOURS:
        raise ValueError("pace must be relaxed, balanced, or full")
    if budget not in {"budget", "moderate", "comfortable"}:
        raise ValueError("budget must be budget, moderate, or comfortable")
    if mobility not in {"standard", "reduced"}:
        raise ValueError("mobility must be standard or reduced")

    parsed_start: date | None = None
    if start_date:
        try:
            parsed_start = date.fromisoformat(start_date)
        except ValueError as exc:
            raise ValueError("start_date must use YYYY-MM-DD") from exc
        month = parsed_start.month
    if end_date:
        if parsed_start is None:
            raise ValueError("start_date is required when end_date is provided")
        try:
            parsed_end = date.fromisoformat(end_date)
        except ValueError as exc:
            raise ValueError("end_date must use YYYY-MM-DD") from exc
        if parsed_end < parsed_start:
            raise ValueError("end_date must not be before start_date")
        days = (parsed_end - parsed_start).days + 1

    trip_days = 2 if days is None else days
    if not 1 <= trip_days <= 14:
        raise ValueError("days must be between 1 and 14")
    if month is not None and not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")

    free_text = requirements.casefold()
    requested_interests = {value.casefold() for value in (interests or []) if value.strip()}
    inferred_interests = _infer_interests(requirements)
    requested_interests.update(inferred_interests)
    if children or any(keyword in free_text for keyword in ("孩子", "儿童", "亲子", "children", "kids")):
        children = True
        requested_interests.add("family")
    if mobility == "standard" and any(keyword in free_text for keyword in ("少走路", "行动不便", "轮椅", "reduced mobility", "wheelchair")):
        mobility = "reduced"
    if budget == "moderate" and any(keyword in free_text for keyword in ("省钱", "低预算", "免费", "budget")):
        budget = "budget"
    if pace == "balanced" and any(keyword in free_text for keyword in ("轻松", "慢慢", "不要太赶", "relaxed", "slow pace")):
        pace = "relaxed"
    elif pace == "balanced" and any(keyword in free_text for keyword in ("充实", "尽量多玩", "特种兵", "full schedule", "packed")):
        pace = "full"

    cities = load_cities()
    if city is None:
        for item in cities:
            aliases = (item["id"], item["name"]["zh"], item["name"]["en"])
            if any(alias.casefold() in free_text for alias in aliases):
                city = item["id"]
                break
    if city is not None and get_city(city) is None:
        raise ValueError(f"Unknown city: {city}")

    wanted_places = [value.strip() for value in (desired_places or []) if value.strip()]
    inferred_place_terms = [
        keyword for keyword in ("熊猫", "panda")
        if keyword in free_text
    ]
    for item in cities:
        for spot in item["spots"]:
            place_labels = [spot["name"]["zh"], spot["name"]["en"], *spot.get("aliases", [])]
            inferred_place_terms.extend(
                label for label in place_labels
                if len(label.strip()) >= 2 and label.casefold() in free_text
            )
    planning_places = list(dict.fromkeys([*wanted_places, *inferred_place_terms]))

    def rank_city(city_item: dict[str, Any]) -> dict[str, Any]:
        explicit = city is not None and _matches_city(city_item, city, None)
        spot_rows: list[tuple[int, dict[str, Any], list[str]]] = []
        for spot in city_item["spots"]:
            if spot.get("availability", {}).get("status") == "temporarily-closed":
                continue
            categories = {value.casefold() for value in spot.get("categories", [])}
            matched = sorted(requested_interests.intersection(categories))
            score = len(matched) * 4
            if planning_places and _spot_matches_terms(spot, planning_places):
                score += 14
            if month is not None and month in spot.get("best_months", []):
                score += 1
            if budget == "budget" and spot.get("ticket", {}).get("price_cny") == 0:
                score += 2
            if mobility == "reduced" and _has_mobility_caution(spot):
                score -= 3
            spot_rows.append((score, spot, matched))

        spot_rows.sort(key=lambda row: (-row[0], row[1]["id"]))
        top_rows = spot_rows[:3]
        score = sum(max(row[0], 0) for row in top_rows)
        coverage_bonus = min(len(spot_rows), 10) / 10
        score += coverage_bonus
        if explicit:
            score += 100
        matched_interest_names = sorted({item for _, _, matched in top_rows for item in matched})
        place_names = [
            row[1]["name"] for row in top_rows
            if planning_places and _spot_matches_terms(row[1], planning_places)
        ]
        reasons: list[dict[str, str]] = []
        if explicit:
            reasons.append({"zh": "符合你指定的目的城市。", "en": "Matches your specified destination city."})
        if place_names:
            reasons.append({"zh": "收录了你明确想去的地点。", "en": "Contains places you explicitly requested."})
        if matched_interest_names:
            reasons.append({"zh": f"与这些兴趣匹配：{'、'.join(matched_interest_names)}。", "en": f"Matches these interests: {', '.join(matched_interest_names)}."})
        if month is not None and any(month in row[1].get("best_months", []) for row in top_rows):
            reasons.append({"zh": f"有适合 {month} 月的已收录地点。", "en": f"Has indexed places suited to month {month}."})
        if not reasons:
            reasons.append({"zh": "当前开放数据覆盖度相对更高。", "en": "Has comparatively stronger coverage in the current open dataset."})
        return {
            "id": city_item["id"],
            "name": city_item["name"],
            "score": round(score, 1),
            "reasons": reasons,
            "matched_spots": [row[1]["name"] for row in top_rows if row[0] > 0],
            "indexed_spot_count": len(city_item["spots"]),
        }

    ranked_cities = sorted((rank_city(item) for item in cities), key=lambda item: (-item["score"], item["id"]))
    selected_rank = ranked_cities[0]
    selected_city = get_city(selected_rank["id"])
    assert selected_city is not None

    itinerary = plan_itinerary(
        selected_city["id"],
        trip_days,
        sorted(requested_interests),
        month=month,
        must_see=planning_places,
        pace=pace,
        mobility=mobility,
    )
    selected_ids = {spot["id"] for day in itinerary["days"] for spot in day["spots"]}
    selected_spots = [
        {**spot, "city": selected_city["name"], "province": selected_city["province"]}
        for spot in selected_city["spots"]
        if spot["id"] in selected_ids
    ]
    matched_place_terms = [
        term for term in wanted_places
        if any(_spot_matches_terms(spot, [term]) for spot in selected_city["spots"])
    ]
    unmatched_place_terms = [term for term in wanted_places if term not in matched_place_terms]

    live_checks = [
        {
            "code": "opening_booking_transport",
            "zh": "逐项核验开放时间、实名预约、护照规则和当天交通。",
            "en": "Verify opening hours, identity-based booking, passport rules, and same-day transport.",
            "sources": selected_city["sources"],
        },
        {
            "code": "live_weather",
            "zh": "临行前查询实时天气和预警；当前仅提供季节性建议。",
            "en": "Check live weather and alerts before departure; current advice is seasonal only.",
            "sources": [selected_city["weather"]["forecast_url"], selected_city["weather"]["warnings_url"]],
        },
        {
            "code": "payment_setup",
            "zh": "出发前准备至少两种支付方式，并核验境外银行卡、移动支付和现金的最新使用说明。",
            "en": "Prepare at least two payment methods and verify current guidance for overseas cards, mobile payments, and cash.",
            "sources": ["https://english.www.gov.cn/news/202404/11/content_WS6617c858c6d0868f4e8e5f4d.html"],
        },
    ]
    if origin_country:
        live_checks.append(
            {
                "code": "international_transport",
                "zh": f"从 {origin_country} 出发的航班、铁路和入境条件需要使用实时官方来源查询。",
                "en": f"Flights, rail options, and entry conditions from {origin_country} require live official sources.",
                "sources": ["https://english.www.gov.cn/services/visitchina/"],
            }
        )
    if traveler_count >= 7:
        live_checks.append(
            {
                "code": "large_group",
                "zh": "较大团队应另行核验团体预约、车辆容量和用餐接待能力。",
                "en": "Larger groups should separately verify group bookings, vehicle capacity, and dining arrangements.",
            }
        )

    confidence = "high" if city or wanted_places else "medium" if requested_interests else "limited"
    return {
        "normalized_requirements": {
            "traveler_count": traveler_count,
            "start_date": start_date,
            "end_date": end_date,
            "month": month,
            "days": trip_days,
            "city": city,
            "desired_places": wanted_places,
            "interests": sorted(requested_interests),
            "inferred_interests": sorted(inferred_interests),
            "pace": pace,
            "budget": budget,
            "mobility": mobility,
            "children": children,
            "origin_country": origin_country,
            "requirements": requirements,
        },
        "recommended_city": {
            **selected_rank,
            "province": selected_city["province"],
            "overview": selected_city["overview"],
            "sources": selected_city["sources"],
            "confidence": confidence,
        },
        "ranked_cities": ranked_cities,
        "itinerary": itinerary,
        "selected_spots": selected_spots,
        "preparation": get_trip_preparation(selected_city["id"], month) if month else None,
        "city_guide": {
            "stay_areas": selected_city["stay_areas"],
            "transport": selected_city["transport"],
            "weather": selected_city["weather"],
            "tourism_portals": selected_city["tourism_portals"],
            "culture": selected_city["culture"],
            "foods": selected_city["foods"],
            "emergency": selected_city["emergency"],
            "sources": selected_city["sources"],
        },
        "matched_requirements": {
            "desired_places": matched_place_terms,
            "interests": sorted(requested_interests),
        },
        "unmet_requirements": [
            {
                "code": "place_not_indexed",
                "value": term,
                "zh": f"当前数据中没有找到“{term}”，请人工核验或补充数据。",
                "en": f"The current dataset did not match '{term}'; verify it manually or add coverage.",
            }
            for term in unmatched_place_terms
        ],
        "live_checks_required": live_checks,
        "automatic_query": {
            "searched_city_count": len(cities),
            "searched_spot_count": sum(len(item["spots"]) for item in cities),
            "method": "explainable-local-ranking",
        },
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
