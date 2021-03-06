"""
Parser for MLB's Gameday XML data
"""


def get_players(tree):
    """Parse players.xml file and return players and their attributes."""
    players = tree.findall(".//player")
    yield from [player.attrib for player in players]


def get_plate_umpire(tree):
    """Parse players.xml data to find the plate umpire."""
    umpires = tree.findall(".//umpire")
    for umpire in umpires:
        if umpire.attrib["position"] == "home":
            return umpire.attrib
    else:
        raise Exception("No plate umpire found.")


def get_game(tree):
    """Parse game.xml data to find the game information."""
    return tree.attrib


def get_teams(tree):
    """Parse game.xml data to find the teams involved."""
    teams = tree.findall(".//team")
    team_count = len(teams)
    if team_count != 2:
        raise Exception("%d teams found" % team_count)

    yield from [team.attrib for team in teams]


def get_stadium(tree):
    """Parse game.xml data to find the stadium."""
    stadium = tree.find(".//stadium")
    if stadium is None:
        raise Exception("Did not find a stadium.")

    return stadium.attrib


def get_atbats(tree):
    """Parse inning_all.xml data to find the atbats and pitches."""
    atbats = tree.findall(".//atbat")
    if not atbats:
        raise Exception("No atbats found.")

    for atbat in atbats:
        pitches = atbat.findall(".//pitch")
        pickoffs = atbat.findall(".//po")
        runners = atbat.findall(".//runner")
        ab = dict(atbat.attrib)
        ab["pitches"] = [pitch.attrib for pitch in pitches]
        ab["pickoffs"] = [po.attrib for po in pickoffs]
        ab["runners"] = [runner.attrib for runner in runners]

        yield ab
