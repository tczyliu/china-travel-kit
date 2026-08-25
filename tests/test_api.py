import unittest

from china_travel_kit.api import health_payload, read_web_asset
from china_travel_kit.store import load_cities


class ApiAssetTests(unittest.TestCase):
    def test_homepage_is_packaged(self) -> None:
        body, content_type = read_web_asset("/")
        self.assertIn("text/html", content_type)
        self.assertIn("华行志".encode(), body)
        self.assertIn(b"v0.4.0", body)
        self.assertIn(b'id="search-form"', body)
        self.assertIn(b'id="recommend-form"', body)
        self.assertIn(b'id="areas-form"', body)
        self.assertIn(b'id="plan-form"', body)
        self.assertIn(b'id="prepare-form"', body)
        self.assertIn(b'id="emergency-form"', body)
        for feature in ("recommend", "search", "areas", "plan", "prepare", "emergency"):
            self.assertIn(f'id="{feature}-tab"'.encode(), body)
        self.assertEqual(body.count(b'class="tab-status">'), 6)
        cities = load_cities()
        total_spots = sum(len(city["spots"]) for city in cities)
        self.assertIn(f'id="spot-count">{total_spots}'.encode(), body)
        categories = {category for city in cities for spot in city["spots"] for category in spot["categories"]}
        for category in categories:
            self.assertIn(f'value="{category}"'.encode(), body)

    def test_stylesheet_is_packaged(self) -> None:
        body, content_type = read_web_asset("/assets/styles.css")
        self.assertIn("text/css", content_type)
        self.assertIn(b"--cinnabar", body)

    def test_javascript_is_packaged(self) -> None:
        body, content_type = read_web_asset("/assets/app.js")
        self.assertIn("text/javascript", content_type)
        self.assertIn(b"generatePlan", body)
        self.assertIn(b"generateRecommendation", body)
        self.assertIn(b"unavailable_spots", body)
        self.assertIn(b"unassigned_spots", body)
        self.assertIn(b"searchAreas", body)
        self.assertIn(b"loadPreparation", body)
        self.assertIn(b"loadEmergency", body)
        self.assertIn("城市文旅官网".encode(), body)
        self.assertIn(b'const API_BASE = window.location.protocol === "file:"', body)
        self.assertNotIn(b"The page is in file preview mode", body)

    def test_favicon_is_packaged(self) -> None:
        body, content_type = read_web_asset("/favicon.svg")
        self.assertIn("image/svg+xml", content_type)
        self.assertIn(b"<svg", body)

    def test_health_payload_exposes_product_version(self) -> None:
        self.assertEqual(health_payload(), {"status": "ok", "name": "huaxingzhi", "version": "0.4.0"})


if __name__ == "__main__":
    unittest.main()
