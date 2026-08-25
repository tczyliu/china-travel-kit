import unittest

from china_travel_kit.store import load_cities
from china_travel_kit.validation import validate_repository


class ValidationTests(unittest.TestCase):
    def test_repository_data_is_valid(self) -> None:
        self.assertEqual(validate_repository(), [])

    def test_priority_city_batch_has_sourced_rating_data(self) -> None:
        cities = {city["id"]: city for city in load_cities()}
        priority_ids = {"beijing", "shanghai", "guangzhou", "shenzhen", "xian", "hangzhou"}
        self.assertTrue(priority_ids <= cities.keys())
        self.assertGreaterEqual(sum(len(city["spots"]) for city in cities.values()), 50)
        for city_id in priority_ids:
            rated = [spot for spot in cities[city_id]["spots"] if spot.get("tourism_rating")]
            self.assertTrue(rated, city_id)
            for spot in rated:
                rating = spot["tourism_rating"]
                self.assertIn(rating["level"], {"5A", "4A"})
                self.assertTrue(rating["source"].startswith("http"))
                self.assertEqual(rating["last_verified"], "2026-08-25")
                self.assertIn("zh", rating["scope_note"])
                self.assertIn("en", rating["scope_note"])

    def test_every_city_has_official_weather_and_alert_entries(self) -> None:
        for city in load_cities():
            with self.subTest(city=city["id"]):
                weather = city["weather"]
                self.assertTrue(weather["forecast_url"].startswith("https://www.weather.com.cn/"))
                self.assertEqual(weather["warnings_url"], "https://www.nmc.cn/publish/alarm.html")
                self.assertIn("zh", weather["provider"])
                self.assertIn("en", weather["provider"])

    def test_every_city_has_a_sourced_culture_tourism_portal(self) -> None:
        for city in load_cities():
            with self.subTest(city=city["id"]):
                self.assertTrue(city["tourism_portals"])
                for portal in city["tourism_portals"]:
                    self.assertTrue(portal["url"].startswith(("https://", "http://")))
                    self.assertIn(".gov.cn", portal["url"])
                    self.assertIn("zh", portal["name"])
                    self.assertIn("en", portal["name"])
                    self.assertEqual(portal["last_verified"], "2026-08-25")


if __name__ == "__main__":
    unittest.main()
