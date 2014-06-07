from urllib.parse import urljoin, urlsplit
import os

from lxml import html
import requests

WEB_ROOT = "http://gd2.mlb.com/components/game/mlb/"


def datetime_to_url(dt):
    """Convert a Python datetime into the date portion of a Gameday URL"""
    return "year_{:04}/month_{:02}/day_{:02}".format(dt.year,
                                                     dt.month, dt.day)


def download(urls, root):
    """Download `urls` into `root`. Return the count of files downloaded.
    Each URL is stored as its full URL (minus the scheme)."""
    session = requests.Session()
    seen_dirs = set()
    downloads = 0
    for url in urls:
        parts = urlsplit(url)
        directory, filename = os.path.split(parts.path)
        # Skip directory pages.
        if not filename:
            continue

        target = os.path.join(root, parts.netloc + directory)
        # Ignore if the target directory already existed.
        os.makedirs(target, exist_ok=True)
        seen_dirs.add(target)

        response = session.get(url)
        response.raise_for_status()

        with open(os.path.join(target, filename), "w") as fh:
            fh.write(response.content.decode("utf8"))
            downloads += 1

    return downloads


def web_scraper(roots, match=None, session=None):
    """Yield URLs in a directory which start with `match`.
    If `match` is None, all links are yielded."""
    for root in roots:
        if session is not None:
            response = session.get(root)
        else:
            response = requests.get(root)
        response.raise_for_status()

        source = html.fromstring(response.content)
        a_tags = source.findall(".//a")
        for a in a_tags:
            url = a.attrib["href"]
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
