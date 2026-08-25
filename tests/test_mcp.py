import unittest

from china_travel_kit.mcp import PROTOCOL_VERSION, handle_request


class McpTests(unittest.TestCase):
    def test_initialize_declares_tools(self) -> None:
        response = handle_request({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        self.assertEqual(response["result"]["protocolVersion"], PROTOCOL_VERSION)
        self.assertIn("tools", response["result"]["capabilities"])

    def test_list_tools(self) -> None:
        response = handle_request({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = {tool["name"] for tool in response["result"]["tools"]}
        self.assertEqual(
            names,
            {
                "search_spots",
                "discover_areas",
                "get_city_guide",
                "plan_itinerary",
                "recommend_trip",
                "get_trip_preparation",
                "get_emergency_help",
                "check_data_freshness",
                "check_package_integrity",
            },
        )

    def test_call_search_tool(self) -> None:
        response = handle_request(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "search_spots", "arguments": {"city": "Beijing", "category": "museum"}},
            }
        )
        self.assertFalse(response["result"].get("isError", False))
        self.assertIn("Palace Museum", response["result"]["content"][0]["text"])

    def test_call_trip_preparation_tool(self) -> None:
        response = handle_request(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "get_trip_preparation", "arguments": {"city": "Lijiang", "month": 8}},
            }
        )
        self.assertFalse(response["result"].get("isError", False))
        self.assertIn("Insect repellent", response["result"]["content"][0]["text"])

    def test_call_recommend_trip_tool(self) -> None:
        response = handle_request(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "recommend_trip",
                    "arguments": {"requirements": "想看熊猫和体验美食", "days": 2},
                },
            }
        )
        self.assertFalse(response["result"].get("isError", False))
        self.assertIn('"id": "chengdu"', response["result"]["content"][0]["text"])

    def test_call_integrity_tool(self) -> None:
        response = handle_request(
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "tools/call",
                "params": {"name": "check_package_integrity", "arguments": {}},
            }
        )
        self.assertFalse(response["result"].get("isError", False))
        self.assertIn('"valid": true', response["result"]["content"][0]["text"])
        self.assertIn('"signature_valid": true', response["result"]["content"][0]["text"])


if __name__ == "__main__":
    unittest.main()
