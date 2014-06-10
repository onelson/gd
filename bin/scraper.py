#! /usr/bin/env python

from datetime import datetime
from urllib.parse import urljoin
import argparse
import asyncio
import functools
import os
import requests
import signal
import sys

from gd import scrape
from gd import utils

def do_input():
    pass


def do_parse():
    pass


def do_scrape(begin=None, end=None):
    """Run the scraper over the range [begin, end]

    If no beginning is given, scraping starts from the root.
    If no ending is given, scraping ends at the current date."""
    begin, begin_parts = utils.get_boundary(begin)
    end, end_parts = utils.get_boundary(end)

    if begin is None:
        start = scrape.WEB_ROOT
    else:
        start = urljoin(scrape.WEB_ROOT,
                        scrape.datetime_to_url(begin, begin_parts))

    if end is None:
        stop = urljoin(scrape.WEB_ROOT,
                       scrape.datetime_to_url(datetime.today()))
    else:
        stop = urljoin(scrape.WEB_ROOT,
                       scrape.datetime_to_url(end, end_parts))

    print("Start: ", start)
    print("Start: ", stop)

    session = requests.Session()

    all_years = scrape.get_years(session=session)

    def get_inclusive_years(years, start, stop):
        in_range = False
        out_range = False
        for year in years:
            if year in start:
                in_range = True
            if year in stop:
               out_range = True
            if in_range:
                yield year
            if out_range:
                break

    inc_years = get_inclusive_years(all_years, start, stop)
    for year in inc_years:
        print(year)


def get_args():
    """Return command line arguments as parsed by argparse."""
    parser = argparse.ArgumentParser(description="blah blah blah")
    parser.add_argument("-b", "--begin", dest="begin", type=str,
                        help="Beginning date in %Y-%m-%d format")
    parser.add_argument("-e", "--end", dest="end", type=str,
                        help="Ending date in %Y-%m-%d format")
    parser.add_argument("-c", "--cache", dest="cache", type=str,
                        help="Local cache directory", default=False)
    parser.add_argument("-d", "--daemon", dest="daemon", action="store_true",
                        default=False, help="Run %(prog)s as a daemon.")

    return parser.parse_args()


def main():
    args = get_args()
    do_scrape(args.begin, args.end)

    if args.daemon:
        run_daemon()


def run_daemon():
    def exiting(signal):
        print("Got signal %s: exiting" % signal)
        loop.stop()

    loop = asyncio.get_event_loop()
    for sig in ("SIGINT", "SIGTERM"):
        loop.add_signal_handler(getattr(signal, sig),
                                functools.partial(exiting, sig))

    print("Event loop running forever, press CTRL+c to interrupt.")
    print("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
    loop.run_forever()


if __name__ == "__main__":
    sys.exit(main())
