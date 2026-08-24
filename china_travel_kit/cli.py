from __future__ import annotations

import argparse
import json
from typing import Any

from .api import serve
from .mcp import run as run_mcp
from .query import freshness_report, plan_itinerary, search_spots
from .store import get_city
from .validation import validate_repository


def _print(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="china-travel", description="Source-aware China inbound travel toolkit")
    commands = parser.add_subparsers(dest="command", required=True)

    search = commands.add_parser("search", help="Search sample travel spots")
    search.add_argument("keyword", nargs="?", default="")
    search.add_argument("--city")
    search.add_argument("--province")
    search.add_argument("--category")
    search.add_argument("--month", type=int, choices=range(1, 13))
    search.add_argument("--free", action="store_true", dest="free_only")
    search.add_argument("--max-hours", type=float)

    city = commands.add_parser("city", help="Show a covered city guide")
    city.add_argument("name")

    plan = commands.add_parser("plan", help="Create a rule-based itinerary draft")
    plan.add_argument("city")
    plan.add_argument("--days", type=int, default=1)
    plan.add_argument("--interests", nargs="*", default=[])

    stale = commands.add_parser("freshness", help="List unverified or stale records")
    stale.add_argument("--days", type=int, default=365)

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
    elif args.command == "freshness":
        _print(freshness_report(args.days))
    elif args.command == "validate":
        errors = validate_repository()
        _print({"valid": not errors, "errors": errors})
        return 1 if errors else 0
    elif args.command == "serve":
        serve(args.host, args.port)
    elif args.command == "mcp":
        run_mcp()
    return 0

