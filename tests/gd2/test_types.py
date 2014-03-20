import unittest

from gd2 import types


class Test_transform(unittest.TestCase):
    """Test the gd2.types.transform function."""

    def test_transform(self):
        actual = {"test1": "lol", "test2": "123", "test3": "0.1"}
        expected = {"test1": "lol", "test2": 123, "test3": 0.1}
        actual_types = {"test1": str, "test2": int, "test3": float}
        types.transform(actual, actual_types)
        self.assertEqual(actual, expected)

    def test_transform_bad_type(self):
        actual = {"test1": "lol"}
        actual_types = {"test1": int}
        self.assertRaises(ValueError, types.transform, actual, actual_types)
