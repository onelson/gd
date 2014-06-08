from datetime import datetime


def get_boundary(date):
    """Format a boundary date.
    This could be a partial date consisting of a year;
    year and month; or year, month, and day."""
    for fmt in ("%Y", "%Y-%m", "%Y-%m-%d"):
        try:
            return datetime.strptime(date, fmt)
        except (TypeError, ValueError):
            continue
    else:
        return None
