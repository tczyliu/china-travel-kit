import unittest
from datetime import date

from china_travel_kit.query import freshness_report, plan_itinerary, search_spots


class QueryTests(unittest.TestCase):
    def test_search_matches_alias_and_city(self) -> None:
        results = search_spots("Forbidden City", city="Beijing")
        self.assertEqual([item["id"] for item in results], ["bj-dongcheng-palace-museum"])

    def test_search_combines_filters(self) -> None:
        results = search_spots(city="成都", category="wildlife", month=4, max_hours=4)
        self.assertEqual([item["id"] for item in results], ["sc-cd-panda-base"])

    def test_plan_prioritizes_interests(self) -> None:
        plan = plan_itinerary("丽江", days=2, interests=["mountain"])
        self.assertEqual(plan["days"][0]["spots"][0]["id"], "yn-lj-yulong-snow-mountain")

    def test_freshness_reports_old_records(self) -> None:
        report = freshness_report(max_age_days=365, today=date(2027, 8, 26))
        self.assertEqual(report["total"], 6)
        self.assertEqual(len(report["stale"]), 6)


if __name__ == "__main__":
    unittest.main()

