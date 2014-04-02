from unittest.mock import MagicMock, patch
from urllib.parse import urljoin
import os
import unittest

from pretend import stub
from requests.exceptions import HTTPError

from gd2 import scrape

class Test_web_scraper(unittest.TestCase):
    """Test gd2.scrape.web_scraper"""

    @patch("requests.get")
    def test_get_exception(self, mock_get):
        mock_get.side_effect = Exception
        rv = scrape.web_scraper(["lol",])
        self.assertRaises(Exception, next, rv)

    @patch("requests.get")
    def test_get_raises_status(self, mock_get):
        response = MagicMock()
        response.raise_for_status.side_effect = HTTPError
        mock_get.return_value = response
        rv = scrape.web_scraper(["lol",])
        self.assertRaises(HTTPError, next, rv)

    @patch("requests.get")
    @patch("gd2.scrape.BeautifulSoup")
    def test_bs_raises(self, mock_BS, mock_get):
        mock_BS.side_effect = Exception
        rv = scrape.web_scraper(["lol",])
        self.assertRaises(Exception, next, rv)

    @patch("requests.get")
    @patch("gd2.scrape.BeautifulSoup")
    def test_no_links(self, mock_BS, mock_get):
        soup = MagicMock()
        soup.find_all.return_value = []
        mock_BS.return_value = soup
        rv = scrape.web_scraper(["lol",])
        self.assertEqual(list(rv), [])

    @patch("requests.get")
    @patch("gd2.scrape.BeautifulSoup")
    def test_matches(self, mock_BS, mock_get):
        root = "http://www.example.com"
        soup = MagicMock()
        link1, link2 = MagicMock(), MagicMock()
        val1, val2 = "foo123", "bar456"

        soup.find_all.return_value = [link1, link2]
        link1.get.return_value = val1
        link2.get.return_value = val2
        mock_BS.return_value = soup

        for match, expected in ((None, [urljoin(root, "foo123"),
                                        urljoin(root, "bar456")]),
                                ("foo", [urljoin(root, "foo123")]),
                                ("lol", [])):
            with self.subTest(match=match):
                rv = scrape.web_scraper([root,], match)
                self.assertEqual(list(rv), expected)

    def test_no_roots(self):
        expected = []
        actual = list(scrape.web_scraper([]))
        self.assertEqual(actual, expected)

    @patch("gd2.scrape.BeautifulSoup")
    def test_requests_session(self, mock_BS):
        response = stub(raise_for_status=lambda: None, content=None)
        session = stub(get=lambda arg: response)

        root = "http://www.example.com"
        soup = MagicMock()
        link1 = MagicMock()
        val1 = "foo123"
        soup.find_all.return_value = [link1]
        link1.get.return_value = val1
        mock_BS.return_value = soup

        expected = [urljoin(root, "foo123")]
        rv = scrape.web_scraper([root], session=session)
        self.assertEqual(list(rv), expected)


class Test_filesystem_scraper(unittest.TestCase):
    """Test gd2.scrape.filesystem_scraper"""

    @patch("os.listdir")
    def test_scraper(self, mock_listdir):
        root = "rootdir"
        file1, file2 = "foo123", "bar456"
        mock_listdir.return_value = [file1, file2]

        for match, expected in ((None, [os.path.join(root, file1),
                                        os.path.join(root, file2)]),
                                ("foo", [os.path.join(root, file1)]),
                                ("lol", [])):
            with self.subTest(match=match):
                rv = scrape.filesystem_scraper([root,], match)
                self.assertEqual(list(rv), expected)

    def test_no_roots(self):
        expected = []
        actual = list(scrape.filesystem_scraper([]))
        self.assertEqual(actual, expected)


class Test_get_urls(unittest.TestCase):
    """Test all gd2.scrape.get_* functions"""

    def test_get(self):
        expected = "abcdefg"
        def fake_scraper(*args):
            yield from expected

        for fn in (scrape.get_years, scrape.get_months, scrape.get_days,
                   scrape.get_games):
            with self.subTest(function=fn):
                actual = fn(["root"], source=fake_scraper)
                self.assertEqual(list(actual), list(expected))

    def test_get_files(self):
        expected = ["players.xml",
                    "game.xml",
                    "inning_all.xml",
                    None,
                    None]

        def fake_scraper(root, match, session):
            """Just yield back the match, make sure we end up with
            the same amount of items."""
            yield from [match]

        actual = scrape.get_files(["root"], source=fake_scraper)
        self.assertEqual(list(actual), list(expected))

