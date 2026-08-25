import unittest
from pathlib import Path

import china_travel_kit


ROOT = Path(__file__).resolve().parents[1]


class SkillPackagingTests(unittest.TestCase):
    def test_skill_has_branded_interface_and_current_workflow(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        interface = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn("# 华行志", skill)
        self.assertIn("tourism_portals", skill)
        self.assertIn('version: "0.4.0"', skill)
        self.assertIn('display_name: "华行志 · China Travel Planner"', interface)
        self.assertIn("$china-travel-kit", interface)

    def test_package_version_is_upgraded(self) -> None:
        self.assertEqual(china_travel_kit.__version__, "0.4.0")


if __name__ == "__main__":
    unittest.main()
