from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .query import freshness_report, plan_itinerary, search_spots
from .store import load_cities


class TravelHandler(BaseHTTPRequestHandler):
    server_version = "ChinaTravelKit/0.1"

    def _send(self, status: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        try:
            if parsed.path == "/health":
                self._send(200, {"status": "ok"})
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
            elif parsed.path == "/plan":
                interests = [value for raw in query.get("interests", []) for value in raw.split(",") if value]
                self._send(200, plan_itinerary(query.get("city", [""])[0], int(query.get("days", ["1"])[0]), interests))
            elif parsed.path == "/freshness":
                self._send(200, freshness_report(int(query.get("days", ["365"])[0])))
            else:
                self._send(404, {"error": "not_found"})
        except (ValueError, TypeError) as exc:
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

