import os

from sportrefpy.nfl.league import NFL
from sportrefpy.nfl.team import NFLFranchise


def all_players():
    players = set()
    nfl = NFL()
    for team in nfl.teams.keys():
        franchise = NFLFranchise(team)
        players.update(franchise.passer_all_time_stats().index)
        players.update(franchise.rusher_all_time_stats().index)
        players.update(franchise.receiving_all_time_stats().index)
        players.update(franchise.returns_all_time_stats().index)
        players.update(franchise.kicking_all_time_stats().index)
        players.update(franchise.scoring_all_time_stats().index)
        players.update(franchise.defense_all_time_stats().index)
    with open(
        os.path.dirname(os.path.dirname(__file__)) + "\\assets\\nfl_players.txt",
        "w",
        encoding="ascii",
    ) as file:
        for player in players:
            try:
                player = player.replace("*", "")
                file.write(f"{player}\n")
            except UnicodeEncodeError:
                continue
