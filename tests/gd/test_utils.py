from datetime import datetime
import unittest

from gd import utils


class Test_get_boundary(unittest.TestCase):

    def test_None(self):
        actual_dt, actual_parts = utils.get_boundary(None)
        self.assertIsNone(actual_dt)
        self.assertEqual(actual_parts, 0)

    def test_empty(self):
        actual_dt, actual_parts = utils.get_boundary("")
        self.assertIsNone(actual_dt)
        self.assertEqual(actual_parts, 0)

    def test_bad_data(self):
        actual_dt, actual_parts = utils.get_boundary("lololololol")
        self.assertIsNone(actual_dt)
        self.assertEqual(actual_parts, 0)

    def test_year(self):
        year = "2014"
        expected_parts = 1
        expected_dt = datetime.strptime(year, "%Y")
        actual_dt, actual_parts = utils.get_boundary(year)
        self.assertEqual(actual_dt, expected_dt)
        self.assertEqual(actual_parts, expected_parts)

    def test_year_month(self):
        year = "2014-07"
        expected_parts = 2
        expected_dt = datetime.strptime(year, "%Y-%m")
        actual_dt, actual_parts = utils.get_boundary(year)
        self.assertEqual(actual_dt, expected_dt)
        self.assertEqual(actual_parts, expected_parts)

    def test_year_month_day(self):
        year = "2014-07-02"
        expected_parts = 3
        expected_dt = datetime.strptime(year, "%Y-%m-%d")
        actual_dt, actual_parts = utils.get_boundary(year)
        self.assertEqual(actual_dt, expected_dt)
        self.assertEqual(actual_parts, expected_parts)


class Test_get_inclusive_urls(unittest.TestCase):

    def _test_range(self, start, stop, expected):
        urls = ["a/a/a", "a/b/a", "a/c/a", "a/d/a", "a/e/a"]
        actual = utils.get_inclusive_urls(urls, start, stop)
        self.assertEqual(list(actual), expected)

    def test_early_range(self):
        start = "a/a"
        stop = "a/c"
        expected = ["a/a/a", "a/b/a", "a/c/a"]
        self._test_range(start, stop, expected)

    def test_middle_range(self):
        start = "a/b"
        stop = "a/d"
        expected = ["a/b/a", "a/c/a", "a/d/a"]
        self._test_range(start, stop, expected)

    def test_late_range(self):
        start = "a/c"
        stop = "a/e"
        expected = ["a/c/a", "a/d/a", "a/e/a"]
        self._test_range(start, stop, expected)

    def test_no_matcing_range(self):
        start = "a/f"
        stop = "a/g"
        expected = []
        self._test_range(start, stop, expected)
