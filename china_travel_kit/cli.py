from __future__ import annotations

import argparse
import json
from typing import Any

from . import __version__
from .api import serve
from .integrity import verify_integrity
from .mcp import run as run_mcp
from .query import (
    discover_areas,
    freshness_report,
    get_emergency_help,
    get_trip_preparation,
    plan_itinerary,
    recommend_trip,
    search_spots,
)
from .store import get_city
from .validation import validate_repository


def _print(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="china-travel", description="Source-aware China inbound travel toolkit")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    search = commands.add_parser("search", help="Search sample travel spots")
    search.add_argument("keyword", nargs="?", default="")
    search.add_argument("--city")
    search.add_argument("--province")
    search.add_argument("--category")
    search.add_argument("--month", type=int, choices=range(1, 13))
    search.add_argument("--free", action="store_true", dest="free_only")
    search.add_argument("--max-hours", type=float)

    areas = commands.add_parser("areas", help="Discover stay areas and attraction neighborhoods")
    areas.add_argument("keyword", nargs="?", default="")
    areas.add_argument("--city")
    areas.add_argument("--province")

    city = commands.add_parser("city", help="Show a covered city guide")
    city.add_argument("name")

    plan = commands.add_parser("plan", help="Create a rule-based itinerary draft")
    plan.add_argument("city")
    plan.add_argument("--days", type=int, default=1)
    plan.add_argument("--interests", nargs="*", default=[])

    recommend = commands.add_parser("recommend", help="Match traveler requirements and create the best covered draft")
    recommend.add_argument("requirements", nargs="?", default="")
    recommend.add_argument("--travelers", type=int, default=1, dest="traveler_count")
    recommend.add_argument("--start-date")
    recommend.add_argument("--end-date")
    recommend.add_argument("--month", type=int, choices=range(1, 13))
    recommend.add_argument("--days", type=int)
    recommend.add_argument("--city")
    recommend.add_argument("--places", nargs="*", default=[], dest="desired_places")
    recommend.add_argument("--interests", nargs="*", default=[])
    recommend.add_argument("--pace", choices=("relaxed", "balanced", "full"), default="balanced")
    recommend.add_argument("--budget", choices=("budget", "moderate", "comfortable"), default="moderate")
    recommend.add_argument("--mobility", choices=("standard", "reduced"), default="standard")
    recommend.add_argument("--children", action="store_true")
    recommend.add_argument("--origin-country")

    prepare = commands.add_parser("prepare", help="Get seasonal preparation guidance")
    prepare.add_argument("city")
    prepare.add_argument("--month", type=int, required=True, choices=range(1, 13))

    emergency = commands.add_parser("emergency", help="Get sourced emergency guidance")
    emergency.add_argument("city")

    stale = commands.add_parser("freshness", help="List unverified or stale records")
    stale.add_argument("--days", type=int, default=365)

    commands.add_parser("integrity", help="Verify that official release files are complete and unchanged")
    commands.add_parser("validate", help="Validate all repository data")

    api = commands.add_parser("serve", help="Run the local HTTP API")
    api.add_argument("--host", default="127.0.0.1")
    api.add_argument("--port", type=int, default=8765)

    commands.add_parser("mcp", help="Run the MCP server over stdio")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "search":
        _print(search_spots(args.keyword, city=args.city, province=args.province, category=args.category, month=args.month, free_only=args.free_only, max_hours=args.max_hours))
    elif args.command == "areas":
        _print(discover_areas(args.keyword, city=args.city, province=args.province))
    elif args.command == "city":
        result = get_city(args.name)
        if result is None:
            _print({"error": f"Unknown city: {args.name}"})
            return 2
        _print(result)
    elif args.command == "plan":
        try:
            _print(plan_itinerary(args.city, args.days, args.interests))
        except ValueError as exc:
            _print({"error": str(exc)})
            return 2
    elif args.command == "recommend":
        try:
            _print(
                recommend_trip(
                    traveler_count=args.traveler_count,
                    start_date=args.start_date,
                    end_date=args.end_date,
                    month=args.month,
                    days=args.days,
                    city=args.city,
                    desired_places=args.desired_places,
                    interests=args.interests,
                    pace=args.pace,
                    budget=args.budget,
                    mobility=args.mobility,
                    children=args.children,
                    origin_country=args.origin_country,
                    requirements=args.requirements,
                )
            )
        except ValueError as exc:
            _print({"error": str(exc)})
            return 2
    elif args.command == "prepare":
        try:
            _print(get_trip_preparation(args.city, args.month))
        except ValueError as exc:
            _print({"error": str(exc)})
            return 2
    elif args.command == "emergency":
        try:
            _print(get_emergency_help(args.city))
        except ValueError as exc:
            _print({"error": str(exc)})
            return 2
    elif args.command == "freshness":
        _print(freshness_report(args.days))
    elif args.command == "integrity":
        result = verify_integrity()
        _print(result)
        return 0 if result["valid"] else 1
    elif args.command == "validate":
        errors = validate_repository()
        _print({"valid": not errors, "errors": errors})
        return 1 if errors else 0
    elif args.command == "serve":
        serve(args.host, args.port)
    elif args.command == "mcp":
        run_mcp()
    return 0
