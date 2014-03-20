"""
Types representing the parts of a game in Gameday.
"""

from datetime import datetime


def _to_datetime(input):
    """Given 2013-05-01T19:38:03Z, convert to Python datetime."""
    value = input[:-1].replace("T", "_")
    return datetime.strptime(value, "%Y-%m-%d_%H:%M:%S")


PITCH_TYPES = {
    'tfs': int,
    'vx0': float,
    'sv_id': str,
    'sz_bot': float,
    'end_speed': float,
    'ax': float,
    'break_length': float,
    'vz0': float,
    'ay': float,
    'spin_rate': float,
    'zone': int,
    'az': float,
    'tfs_zulu': _to_datetime,
    'mt': str,
    'nasty': int,
    'cc': str,
    'pitch_type': str,
    'type': str,
    'type_confidence': float,
    'x': float,
    'sz_top': float,
    'break_angle': float,
    'id': int,
    'z0': float,
    'break_y': float,
    'y0': float,
    'x0': float,
    'des_es': str,
    'spin_dir': float,
    'start_speed': float,
    'y': float,
    'vy0': float,
    'pfx_z': float,
    'pfx_x': float,
    'pz': float,
    'des': str,
    'px': float
}


ATBAT_TYPES = {
    'b': int,
    'b_height': str,
    'batter': int,
    'des': str,
    'des_es': str,
    'event': str,
    'num': int,
    'o': int,
    'p_throws': str,
    'pitcher': int,
    's': int,
    'stand': str,
    'start_tfs': int,
    'start_tfs_zulu': _to_datetime
}


class AtBat(object):
    """An at bat."""

    def __init__(self, **attribs):
        self.pitches = []
        for attr, raw_val in attribs.items():
            val = ATBAT_TYPES[attr](raw_val)
            setattr(self, attr, val)


class Pitch(object):
    """A pitch."""

    def __init__(self, **attribs):
        for attr, raw_val in attribs.items():
            val = PITCH_TYPES[attr](raw_val)
            setattr(self, attr, val)
