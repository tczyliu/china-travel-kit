import unittest

from china_travel_kit.validation import validate_repository


class ValidationTests(unittest.TestCase):
    def test_repository_data_is_valid(self) -> None:
        self.assertEqual(validate_repository(), [])


if __name__ == "__main__":
    unittest.main()

