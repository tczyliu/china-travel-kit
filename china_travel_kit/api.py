from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from . import __version__
from .query import (
    discover_areas,
    freshness_report,
    get_emergency_help,
    get_trip_preparation,
    plan_itinerary,
    recommend_trip,
    search_spots,
)
from .store import WEB_DIR, load_cities


WEB_ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/assets/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/assets/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/favicon.svg": ("favicon.svg", "image/svg+xml; charset=utf-8"),
}


def health_payload() -> dict[str, str]:
    return {"status": "ok", "name": "huaxingzhi", "version": __version__}


def read_web_asset(path: str) -> tuple[bytes, str]:
    filename, content_type = WEB_ASSETS[path]
    return (WEB_DIR / filename).read_bytes(), content_type


class TravelHandler(BaseHTTPRequestHandler):
    server_version = f"Huaxingzhi/{__version__}"

    def _send_local_file_cors(self) -> None:
        if self.headers.get("Origin") != "null":
            return
        self.send_header("Access-Control-Allow-Origin", "null")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        if self.headers.get("Access-Control-Request-Private-Network") == "true":
            self.send_header("Access-Control-Allow-Private-Network", "true")

    def _send_bytes(self, status: int, body: bytes, content_type: str, *, cache: bool = False) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "public, max-age=3600" if cache else "no-cache")
        self._send_local_file_cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self._send_local_file_cors()
        self.end_headers()

    def _send(self, status: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        try:
            if parsed.path in WEB_ASSETS:
                body, content_type = read_web_asset(parsed.path)
                self._send_bytes(200, body, content_type, cache=parsed.path.startswith("/assets/"))
            elif parsed.path == "/health":
                self._send(200, health_payload())
            elif parsed.path == "/cities":
                self._send(200, [{"id": city["id"], "name": city["name"]} for city in load_cities()])
            elif parsed.path == "/search":
                results = search_spots(
                    query.get("q", [""])[0],
                    city=query.get("city", [None])[0],
                    category=query.get("category", [None])[0],
                    month=int(query["month"][0]) if "month" in query else None,
                    free_only=query.get("free", ["false"])[0].lower() == "true",
                    max_hours=float(query["max_hours"][0]) if "max_hours" in query else None,
                )
                self._send(200, {"count": len(results), "results": results})
            elif parsed.path == "/areas":
                results = discover_areas(
                    query.get("q", [""])[0],
                    city=query.get("city", [None])[0],
                    province=query.get("province", [None])[0],
                )
                self._send(200, {"count": len(results), "results": results})
            elif parsed.path == "/plan":
                interests = [value for raw in query.get("interests", []) for value in raw.split(",") if value]
                self._send(200, plan_itinerary(query.get("city", [""])[0], int(query.get("days", ["1"])[0]), interests))
            elif parsed.path == "/recommend":
                interests = [value for raw in query.get("interests", []) for value in raw.split(",") if value]
                desired_places = [value for raw in query.get("desired_places", []) for value in raw.split(",") if value]
                self._send(
                    200,
                    recommend_trip(
                        traveler_count=int(query.get("traveler_count", ["1"])[0]),
                        start_date=query.get("start_date", [None])[0],
                        end_date=query.get("end_date", [None])[0],
                        month=int(query["month"][0]) if "month" in query else None,
                        days=int(query["days"][0]) if "days" in query else None,
                        city=query.get("city", [None])[0],
                        desired_places=desired_places,
                        interests=interests,
                        pace=query.get("pace", ["balanced"])[0],
                        budget=query.get("budget", ["moderate"])[0],
                        mobility=query.get("mobility", ["standard"])[0],
                        children=query.get("children", ["false"])[0].lower() == "true",
                        origin_country=query.get("origin_country", [None])[0],
                        requirements=query.get("requirements", [""])[0],
                    ),
                )
            elif parsed.path == "/prepare":
                self._send(200, get_trip_preparation(query.get("city", [""])[0], int(query.get("month", ["0"])[0])))
            elif parsed.path == "/emergency":
                self._send(200, get_emergency_help(query.get("city", [""])[0]))
            elif parsed.path == "/freshness":
                self._send(200, freshness_report(int(query.get("days", ["365"])[0])))
            else:
                self._send(404, {"error": "not_found"})
        except (OSError, ValueError, TypeError) as exc:
            self._send(400, {"error": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), TravelHandler)
    print(f"China Travel Kit API listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
