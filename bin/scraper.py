#! /usr/bin/env python

from datetime import datetime
from urllib.parse import urljoin
import argparse
import asyncio
import functools
import os
import signal
import sys

from gd import scrape
from gd import utils

def do_input():
    pass


def do_parse():
    pass


def do_scrape(args):
    start = utils.get_boundary(args.start)
    end = utils.get_boundary(args.end)

    if start is None:
        root = scrape.WEB_ROOT
    else:
        root = urljoin(scrape.WEB_ROOT, scrape.datetime_to_url(start))

    stop = None
    if end:
        stop = urljoin(scrape.WEB_ROOT, scrape.datetime_to_url(end))

def get_args():
    """Return command line arguments as parsed by argparse."""
    parser = argparse.ArgumentParser(description="blah blah blah")
    parser.add_argument("-s", "--start", dest="start", type=str,
                        help="Start date in %Y-%m-%d format")
    parser.add_argument("-e", "--end", dest="end", type=str,
                        help="End date in %Y-%m-%d format")
    parser.add_argument("-c", "--cache", dest="cache", type=str,
                        help="Local cache directory", default=False)
    parser.add_argument("-d", "--daemon", dest="daemon", action="store_true",
                        default=False, help="Run %(prog)s as a daemon.")

    return parser.parse_args()


def main():
    args = get_args()
    print(args)
    do_scrape(args)

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
