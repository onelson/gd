from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

ROOT = "http://gd2.mlb.com/components/game/mlb/"


def _get_urls(roots, match):
    """Given a list of roots, iterate through them and yield links that match.
    If `match` is None, all links are yielded."""
    for root in roots:
        print(requests)
        response = requests.get(root)
        response.raise_for_status()

        bs = BeautifulSoup(response.content, "lxml")
        for link in bs.find_all("a"):
            url = link.get("href")
            if match is None or url[slice(0, len(match))] == match:
                yield urljoin(root, url)


def get_years(root=ROOT):
    """From the root URL, yield URLs to the available years."""
    yield from _get_urls([root], "year")


def get_months(years):
    """Yield URLs to the available months for every year."""
    yield from _get_urls(years, "month")


def get_days(months):
    """Yield URLs to the available days for every month."""
    yield from _get_urls(months, "day")


def get_games(days):
    """Yield URLs to the available games for every day."""
    yield from _get_urls(days, "gid")


def get_files(games):
    """Yield URLs to the relevant files for every game."""
    for game in games:
        yield from _get_urls([game], "players.xml")
        yield from _get_urls([game], "game.xml")
        yield from _get_urls([urljoin(game, "inning")], "inning_all.xml")

        # Go another directory deep and get all pitchers and all batters.
        pitchers = _get_urls([game], "pitchers")
        yield from _get_urls(pitchers, None)

        batters = _get_urls([game], "batters")
        yield from _get_urls(batters, None)
