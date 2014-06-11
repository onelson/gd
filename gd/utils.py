from datetime import datetime


def get_boundary(date):
    """Format a boundary date string and return the datetime and the number
    of parts the datetime object was constructed from.

    This could be a partial date consisting of a year;
    year and month; or year, month, and day."""
    parts = 0
    for fmt in ("%Y", "%Y-%m", "%Y-%m-%d"):
        try:
            parts += 1
            return datetime.strptime(date, fmt), parts
        except (TypeError, ValueError):
            continue
    else:
        return None, 0


def get_inclusive_urls(urls, start, stop):
    """Yield URLs which are of the range [start, stop]"""
    in_range = False
    out_range = False
    for url in urls:
        # Check both that a URL contains or is contained within one of
        # the boundaries. This is necessary as deeper links come.
        if url in start or start in url:
            in_range = True
        if url in stop or stop in url:
            out_range = True
        if in_range:
            yield url
        if out_range:
            break
