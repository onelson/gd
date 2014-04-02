from urllib.parse import urljoin
import itertools
import os

from bs4 import BeautifulSoup
import requests

WEB_ROOT = "http://gd2.mlb.com/components/game/mlb/"


def web_scraper(roots, match=None, session=None):
    """Yield URLs in a directory which start with `match`.
    If `match` is None, all links are yielded."""
    for root in roots:
        if session is not None:
            response = session.get(root)
        else:
            response = requests.get(root)
        response.raise_for_status()

        bs = BeautifulSoup(response.content, "lxml")
        for link in bs.find_all("a"):
            url = link.get("href")
            if match is None or url[slice(0, len(match))] == match:
                yield urljoin(root, url)


def filesystem_scraper(roots, match=None, **kwargs):
    """Yield paths in a directory which start with `match`.
    If `match` is None, all files are yielded."""
    for root in roots:
        for name in os.listdir(root):
            if match is None or name.startswith(match):
                yield os.path.join(root, name)


def get_years(root=WEB_ROOT, source=web_scraper, session=None):
    """From the root URL, yield URLs to the available years."""
    yield from source([root], "year", session)


def get_months(years, source=web_scraper, session=None):
    """Yield URLs to the available months for every year."""
    yield from source(years, "month", session)


def get_days(months, source=web_scraper, session=None):
    """Yield URLs to the available days for every month."""
    yield from source(months, "day", session)


def get_games(days, source=web_scraper, session=None):
    """Yield URLs to the available games for every day."""
    yield from source(days, "gid", session)


def get_files(games, source=web_scraper, session=None):
    """Yield URLs to the relevant files for every game."""
    for game in games:
        yield from source([game], "players.xml", session)
        yield from source([game], "game.xml", session)
        yield from source([urljoin(game, "inning")],
                          "inning_all.xml", session)

        # Go another directory deep and get all pitchers and all batters.
        pitchers = source([game], "pitchers", session)
        yield from source(pitchers, None, session)

        batters = source([game], "batters", session)
        yield from source(batters, None, session)
