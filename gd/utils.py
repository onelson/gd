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
