from __future__ import annotations

import json
import sys
from typing import Any, TextIO

from .query import freshness_report, plan_itinerary, search_spots
from .store import get_city


PROTOCOL_VERSION = "2025-11-25"


TOOLS = [
    {
        "name": "search_spots",
        "title": "Search China travel spots",
        "description": "Search source-aware sample travel data. Results are not live availability or navigation data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string"},
                "city": {"type": "string"},
                "category": {"type": "string"},
                "month": {"type": "integer", "minimum": 1, "maximum": 12},
                "free_only": {"type": "boolean"},
                "max_hours": {"type": "number", "minimum": 0},
            },
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "get_city_guide",
        "title": "Get a city guide",
        "description": "Get transport, seasonal, food, culture, stay-area, and emergency guidance for a covered city.",
        "inputSchema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "plan_itinerary",
        "title": "Draft a city itinerary",
        "description": "Create an explainable rule-based draft. Always verify live hours, bookings, weather, and transport.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "days": {"type": "integer", "minimum": 1, "maximum": 14, "default": 1},
                "interests": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["city"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "check_data_freshness",
        "title": "Check travel data freshness",
        "description": "List unverified or stale records so callers can avoid presenting old facts as current.",
        "inputSchema": {
            "type": "object",
            "properties": {"max_age_days": {"type": "integer", "minimum": 1, "default": 365}},
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
]


def _tool_result(payload: Any, *, is_error: bool = False) -> dict[str, Any]:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    result: dict[str, Any] = {"content": [{"type": "text", "text": text}]}
    if is_error:
        result["isError"] = True
    return result


def handle_request(message: dict[str, Any]) -> dict[str, Any] | None:
    if "id" not in message:
        return None
    request_id = message["id"]
    method = message.get("method")
    params = message.get("params") or {}
    try:
        if method == "initialize":
            result = {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "china-travel-kit", "version": "0.2.0"},
                "instructions": "Sample, source-aware travel data. Verify stale records and all live conditions before travel.",
            }
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments") or {}
            if name == "search_spots":
                result = _tool_result(search_spots(**args))
            elif name == "get_city_guide":
                city = get_city(args.get("city", ""))
                result = _tool_result(city if city else {"error": "unknown_city"}, is_error=city is None)
            elif name == "plan_itinerary":
                result = _tool_result(plan_itinerary(args["city"], args.get("days", 1), args.get("interests", [])))
            elif name == "check_data_freshness":
                result = _tool_result(freshness_report(args.get("max_age_days", 365)))
            else:
                result = _tool_result({"error": f"unknown_tool: {name}"}, is_error=True)
        else:
            return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "Method not found"}}
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    except (KeyError, TypeError, ValueError) as exc:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32602, "message": str(exc)}}


def run(stdin: TextIO = sys.stdin, stdout: TextIO = sys.stdout) -> None:
    for line in stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            response = handle_request(message)
        except json.JSONDecodeError as exc:
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}
        if response is not None:
            stdout.write(json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n")
            stdout.flush()
