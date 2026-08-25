import unittest
from datetime import date

from china_travel_kit.query import (
    discover_areas,
    freshness_report,
    get_emergency_help,
    get_trip_preparation,
    plan_itinerary,
    recommend_trip,
    search_spots,
)


class QueryTests(unittest.TestCase):
    def test_search_matches_alias_and_city(self) -> None:
        results = search_spots("Forbidden City", city="Beijing")
        self.assertEqual([item["id"] for item in results], ["bj-dongcheng-palace-museum"])
        self.assertTrue(results[0]["tourism_portals"][0]["url"].startswith("https://"))

    def test_search_combines_filters(self) -> None:
        results = search_spots(city="成都", category="wildlife", month=4, max_hours=4)
        self.assertEqual([item["id"] for item in results], ["sc-cd-panda-base"])

    def test_new_priority_city_landmarks_are_searchable(self) -> None:
        cases = {
            "上海博物馆": "Shanghai",
            "兵马俑": "Xi'an",
            "西湖": "Hangzhou",
            "广州塔": "Guangzhou",
            "世界之窗": "Shenzhen",
        }
        for keyword, city_id in cases.items():
            with self.subTest(keyword=keyword):
                results = search_spots(keyword)
                self.assertTrue(results)
                self.assertEqual(results[0]["city"]["en"], city_id)

    def test_recommendation_matches_new_city_from_named_place(self) -> None:
        result = recommend_trip(requirements="第一次来中国，想去兵马俑和陕西历史博物馆", days=2)
        self.assertEqual(result["recommended_city"]["id"], "xian")

    def test_chengdu_has_release_ready_sample_depth(self) -> None:
        self.assertGreaterEqual(len(search_spots(city="成都")), 15)

    def test_plan_prioritizes_interests(self) -> None:
        plan = plan_itinerary("丽江", days=2, interests=["mountain"])
        self.assertEqual(plan["days"][0]["spots"][0]["id"], "yn-lj-yulong-snow-mountain")

    def test_large_plan_respects_daily_limit_and_keeps_bilingual_output(self) -> None:
        plan = plan_itinerary("成都", days=2, interests=["wildlife", "culture"])
        self.assertTrue(all(day["estimated_hours"] <= 8 for day in plan["days"]))
        self.assertTrue(plan["unassigned_spots"])
        self.assertIn("zh", plan["days"][0]["spots"][0]["neighborhood"])
        self.assertIn("zh", plan["planning_notes"][0])
        self.assertEqual([item["id"] for item in plan["unavailable_spots"]], ["sc-cd-jinsha-site-museum"])
        planned_ids = {spot["id"] for day in plan["days"] for spot in day["spots"]}
        self.assertNotIn("sc-cd-jinsha-site-museum", planned_ids)
        day_ids = [{spot["id"] for spot in day["spots"]} for day in plan["days"]]
        self.assertTrue(any({"sc-cd-panda-base", "sc-cd-eastern-suburb-memory"} <= ids for ids in day_ids))
        self.assertTrue(any({"sc-cd-jinli-street", "sc-cd-wuhou-shrine"} <= ids for ids in day_ids))
        first_spot = plan["days"][0]["spots"][0]
        self.assertIn("zh", first_spot["cultural_context"])
        self.assertTrue(first_spot["nearby_spots"])
        self.assertEqual(len(first_spot["amenities_guidance"]), 4)
        self.assertIn("arrival_guidance", plan["days"][0])
        self.assertIn("transfers", plan["days"][0])
        self.assertTrue(plan["recommended_stay_areas"])
        self.assertTrue(plan["weather"]["forecast_url"].startswith("https://"))
        self.assertTrue(plan["tourism_portals"])

    def test_discover_areas_returns_bilingual_stay_area(self) -> None:
        results = discover_areas("东城", city="Beijing")
        self.assertEqual([item["id"] for item in results], ["dongcheng"])
        self.assertEqual(results[0]["name"]["en"], "Dongcheng")
        self.assertEqual(results[0]["indexed_spot_count"], 2)
        self.assertIn("开放数据集", results[0]["coverage_note"]["zh"])

    def test_chengdu_stay_areas_have_indexed_places(self) -> None:
        results = [item for item in discover_areas(city="成都") if item["kind"] == "stay-area"]
        counts = {item["id"]: item["indexed_spot_count"] for item in results}
        self.assertGreater(counts["tianfu-square"], 0)
        self.assertGreater(counts["yulin"], 0)
        self.assertTrue(all("spot_count" not in item for item in results))

    def test_trip_preparation_selects_month(self) -> None:
        result = get_trip_preparation("成都", 7)
        self.assertEqual(result["seasonal_advice"][0]["gear"][1]["en"], "Insect repellent")
        self.assertIn("实时天气", result["limitations"]["zh"])
        self.assertEqual(result["transport"]["local"][0]["zh"], "地铁")
        self.assertIn("zh", result["foods"][0]["dietary_notes"][0])
        self.assertIn("weather.com.cn", result["weather"]["forecast_url"])
        self.assertIn("nmc.cn", result["weather"]["warnings_url"])

    def test_recommend_trip_infers_city_dates_and_free_text(self) -> None:
        result = recommend_trip(
            traveler_count=2,
            start_date="2026-07-10",
            end_date="2026-07-12",
            requirements="第一次来中国，想看熊猫、吃美食，行程轻松一些",
        )
        self.assertEqual(result["recommended_city"]["id"], "chengdu")
        self.assertEqual(result["normalized_requirements"]["month"], 7)
        self.assertEqual(result["normalized_requirements"]["days"], 3)
        self.assertEqual(result["normalized_requirements"]["pace"], "relaxed")
        planned_ids = [spot["id"] for day in result["itinerary"]["days"] for spot in day["spots"]]
        self.assertIn("sc-cd-panda-base", planned_ids)
        panda = next(spot for spot in result["selected_spots"] if spot["id"] == "sc-cd-panda-base")
        self.assertTrue(panda["sources"][0].startswith("https://"))
        self.assertIn("summary", panda)
        self.assertTrue(all(day["estimated_hours"] <= 4 for day in result["itinerary"]["days"]))
        self.assertEqual(result["preparation"]["seasonal_advice"][0]["gear"][1]["en"], "Insect repellent")

    def test_recommend_trip_explains_mobility_cautions_and_live_checks(self) -> None:
        result = recommend_trip(
            desired_places=["玉龙雪山"],
            days=2,
            mobility="reduced",
            origin_country="Singapore",
        )
        self.assertEqual(result["recommended_city"]["id"], "lijiang")
        self.assertTrue(result["itinerary"]["caution_spots"])
        self.assertTrue(
            all(
                day["estimated_hours"] <= result["itinerary"]["daily_limit_hours"]
                for day in result["itinerary"]["days"]
            )
        )
        self.assertTrue(any(item["code"] == "international_transport" for item in result["live_checks_required"]))
        self.assertTrue(any(item["code"] == "payment_setup" for item in result["live_checks_required"]))
        weather_check = next(item for item in result["live_checks_required"] if item["code"] == "live_weather")
        self.assertEqual(len(weather_check["sources"]), 2)

    def test_relaxed_plan_keeps_an_explicit_long_visit_as_a_visible_exception(self) -> None:
        result = recommend_trip(
            desired_places=["玉龙雪山"],
            days=2,
            pace="relaxed",
            mobility="reduced",
            requirements="还想在古城摄影，需要减少步行和台阶",
        )
        itinerary = result["itinerary"]
        planned_ids = [spot["id"] for day in itinerary["days"] for spot in day["spots"]]
        self.assertIn("yn-lj-yulong-snow-mountain", planned_ids)
        self.assertTrue(itinerary["pace_exceptions"])
        self.assertEqual(itinerary["pace_exceptions"][0]["spot"]["zh"], "玉龙雪山")
        self.assertTrue(any(day["pace_exception"] for day in itinerary["days"]))

    def test_recommend_trip_rejects_invalid_date_range(self) -> None:
        with self.assertRaisesRegex(ValueError, "end_date"):
            recommend_trip(start_date="2026-08-10", end_date="2026-08-09")

    def test_recommend_trip_uses_named_place_from_free_text_for_city_ranking(self) -> None:
        result = recommend_trip(requirements="想去玉龙雪山，少走路", days=2)
        self.assertEqual(result["recommended_city"]["id"], "lijiang")
        self.assertEqual(result["normalized_requirements"]["mobility"], "reduced")

    def test_emergency_help_includes_source_and_scope(self) -> None:
        result = get_emergency_help("丽江")
        police = result["services"][0]
        self.assertEqual(police["phone"], "110")
        self.assertTrue(police["source"].startswith("https://"))
        self.assertEqual(police["scope"], "Chinese mainland")

    def test_freshness_reports_old_records(self) -> None:
        report = freshness_report(max_age_days=365, today=date(2027, 8, 26))
        self.assertGreaterEqual(report["total"], 50)
        self.assertEqual(len(report["stale"]), report["total"])


if __name__ == "__main__":
    unittest.main()
