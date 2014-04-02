from urllib.parse import urljoin
import itertools
import os

from bs4 import BeautifulSoup
import requests

WEB_ROOT = "http://gd2.mlb.com/components/game/mlb/"


def web_scraper(roots, match=None):
    """Yield URLs in a directory which start with `match`.
    If `match` is None, all links are yielded."""
    for root in roots:
        response = requests.get(root)
        response.raise_for_status()

        bs = BeautifulSoup(response.content, "lxml")
        for link in bs.find_all("a"):
            url = link.get("href")
            if match is None or url[slice(0, len(match))] == match:
                yield urljoin(root, url)


def filesystem_scraper(roots, match=None):
    """Yield paths in a directory which start with `match`.
    If `match` is None, all files are yielded."""
    for root in roots:
        for name in os.listdir(root):
            if match is None or name.startswith(match):
                yield os.path.join(root, name)


def get_years(root=WEB_ROOT, source=web_scraper):
    """From the root URL, yield URLs to the available years."""
    yield from source([root], "year")


def get_months(years, source=web_scraper):
    """Yield URLs to the available months for every year."""
    yield from source(years, "month")


def get_days(months, source=web_scraper):
    """Yield URLs to the available days for every month."""
    yield from source(months, "day")


def get_games(days, source=web_scraper):
    """Yield URLs to the available games for every day."""
    yield from source(days, "gid")


def get_files(games, source=web_scraper):
    """Yield URLs to the relevant files for every game."""
    for game in games:
        yield from source([game], "players.xml")
        yield from source([game], "game.xml")
        yield from source([urljoin(game, "inning")], "inning_all.xml")

        # Go another directory deep and get all pitchers and all batters.
        pitchers = source([game], "pitchers")
        yield from source(pitchers, None)

        batters = source([game], "batters")
        yield from source(batters, None)
