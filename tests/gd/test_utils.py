from datetime import datetime
import unittest

from gd import utils


class Test_get_boundary(unittest.TestCase):

    def test_None(self):
        actual = utils.get_boundary(None)
        self.assertIsNone(actual)

    def test_empty(self):
        actual = utils.get_boundary("")
        self.assertIsNone(actual)

    def test_bad_data(self):
        actual = utils.get_boundary("lololololol")
        self.assertIsNone(actual)

    def test_year(self):
        year = "2014"
        expected = datetime.strptime(year, "%Y")
        actual = utils.get_boundary(year)
        self.assertEqual(actual, expected)

    def test_year_month(self):
        year = "2014-07"
        expected = datetime.strptime(year, "%Y-%m")
        actual = utils.get_boundary(year)
        self.assertEqual(actual, expected)

    def test_year_month_day(self):
        year = "2014-07-02"
        expected = datetime.strptime(year, "%Y-%m-%d")
        actual = utils.get_boundary(year)
        self.assertEqual(actual, expected)
