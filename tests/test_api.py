import unittest

from china_travel_kit.api import read_web_asset


class ApiAssetTests(unittest.TestCase):
    def test_homepage_is_packaged(self) -> None:
        body, content_type = read_web_asset("/")
        self.assertIn("text/html", content_type)
        self.assertIn("华行志".encode(), body)
        self.assertIn(b'id="search-form"', body)

    def test_stylesheet_is_packaged(self) -> None:
        body, content_type = read_web_asset("/assets/styles.css")
        self.assertIn("text/css", content_type)
        self.assertIn(b"--cinnabar", body)

    def test_javascript_is_packaged(self) -> None:
        body, content_type = read_web_asset("/assets/app.js")
        self.assertIn("text/javascript", content_type)
        self.assertIn(b"generatePlan", body)


if __name__ == "__main__":
    unittest.main()
