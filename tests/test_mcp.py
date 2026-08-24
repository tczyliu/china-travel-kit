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
        self.assertEqual(names, {"search_spots", "get_city_guide", "plan_itinerary", "check_data_freshness"})

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


if __name__ == "__main__":
    unittest.main()

