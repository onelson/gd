from pretend import stub

import unittest

from gd2 import parser


class Test_simple_get(unittest.TestCase):
    """Test the gd2.parser functions which just return attributes."""

    def test_get(self):
        for func in (parser.get_player, parser.get_game):
            with self.subTest(function=func):
                expected = "test"
                s = stub(attrib=expected)
                actual = func(s)
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


class Test_get_teams(unittest.TestCase):
    """Test the gd2.parser.get_teams function."""

    def test_get_teams(self):
        value = "team name"
        team = stub(attrib=value)
        tree = stub(findall=lambda arg: [team, team])
        actual = parser.get_teams(tree)
        self.assertEqual(actual, [value, value])

    def test_get_teams_not_two_teams(self):
        value = "team name"
        team = stub(attrib=value)

        # We should only ever get two teams.
        for teams in ([], [team, team, team]):
            with self.subTest(teams=teams):
                tree = stub(findall=lambda arg: teams)
                self.assertRaises(parser.ParseError, parser.get_teams, tree)


class Test_get_stadium(unittest.TestCase):
    """Test the gd2.parser.get_stadium function."""

    def test_get_stadium(self):
        expected = "Wrigley Field"
        stadium = stub(attrib=expected)
        tree = stub(find=lambda arg: stadium)
        actual = parser.get_stadium(tree)
        self.assertEqual(actual, expected)

    def test_get_stadium_missing(self):
        tree = stub(find=lambda arg: None)
        self.assertRaises(parser.ParseError, parser.get_stadium, tree)


class Test_get_atbats(unittest.TestCase):
    """Test the gd2.parser.get_atbats function."""

    def test_get_atbats_no_atbats(self):
        tree = stub(findall=lambda arg: [])
        self.assertRaises(parser.ParseError, parser.get_atbats, tree)
