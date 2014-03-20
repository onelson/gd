from pretend import stub

import unittest

from gd2 import parser


class Test_get_player(unittest.TestCase):
    """Test the gd2.parser.get_player function."""

    def test_get_player(self):
        expected = "Greg Maddux"
        s = stub(attrib=expected)
        actual = parser.get_player(s)
        self.assertEqual(actual, expected)


class Test_get_plate_umpire(unittest.TestCase):
    """Test the gd2.parser.get_plate_umpire function."""

    def test_get_plate_umpire(self):
        expected = {"position": "home", "name": "Gerry Davis"}
        element = stub(attrib=expected)
        tree = stub(findall=lambda arg: [element])
        actual = parser.get_plate_umpire(tree)
        self.assertEqual(actual, expected)

    def test_get_plate_umpire_no_pu(self):
        expected = {"position": "first", "name": "Ted Barrett"}
        element = stub(attrib=expected)
        tree = stub(findall=lambda arg: [element])
        self.assertRaises(parser.ParseError, parser.get_plate_umpire, tree)

    def test_get_plate_umpire_no_umpires(self):
        tree = stub(findall=lambda arg: [])
        self.assertRaises(parser.ParseError, parser.get_plate_umpire, tree)
