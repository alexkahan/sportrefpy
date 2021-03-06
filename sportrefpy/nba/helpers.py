import os

from sportrefpy.nba.league import NBA
from sportrefpy.nba.team import NBAFranchise


def all_players():
    players = set()
    nba = NBA()
    for team in nba.teams.keys():
        franchise = NBAFranchise(team)
        players.update(franchise.players_all_time_stats().index)
    with open(
        os.path.dirname(os.path.dirname(__file__)) + "\\assets\\nba_players.txt",
        "w",
        encoding="ascii",
    ) as file:
        for player in players:
            try:
                file.write(f"{player}\n")
            except UnicodeEncodeError:
                continue
