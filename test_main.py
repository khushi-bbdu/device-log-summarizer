
import unittest

from main import clean_readings


class TestCleanReadings(unittest.TestCase):

    def test_mixed_values(self):
        values = [10, "25.5", None, -4, 700]
        expected = [10.0, 25.5, 500.0]

        self.assertEqual(clean_readings(values), expected)

    def test_all_invalid_values(self):
        values = ["hello", None, -10]
        expected = []

        self.assertEqual(clean_readings(values), expected)

    def test_empty_list(self):
        self.assertEqual(clean_readings([]), [])


if __name__ == "__main__":
    unittest.main()
