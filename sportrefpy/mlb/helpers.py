import os

from sportrefpy.mlb.league import MLB
from sportrefpy.mlb.team import MLBTeam


def all_players():
    players = set()
    mlb = MLB()
    for team in mlb.teams.keys():
        franchise = MLBTeam(team)
        players.update(franchise.pitchers_all_time_stats().index)
        players.update(franchise.batters_all_time_stats().index)
    with open(
        os.path.dirname(os.path.dirname(__file__)) + "\\assets\\mlb_players.txt",
        "w",
        encoding="ascii",
    ) as file:
        for player in players:
            try:
                file.write(f"{player}\n")
            except UnicodeEncodeError:
                continue
