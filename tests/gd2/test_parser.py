from pretend import stub

import unittest

from gd2 import parser


class Test_get_player(unittest.TestCase):
    """Test the gd2.parser.get_player function."""

    def test_get_player(self):
        expected = "test"
        s = stub(attrib=expected)
        actual = parser.get_player(s)
        self.assertEqual(actual, expected)
