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
