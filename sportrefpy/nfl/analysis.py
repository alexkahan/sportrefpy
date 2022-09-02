import pandas as pd

from sportrefpy.nfl.team import NFLTeam

# from sportrefpy.nfl.player import NFLPlayer


def compare_franchises(teams):
    teams = [NFLTeam(team) for team in teams]
    comparison = pd.concat(
        [team.season_history()[["W", "L", "T"]].sum() for team in teams], axis=1
    )
    comparison.columns = [team.franchise_name for team in teams]
    comparison = comparison.transpose()
    comparison["W%"] = comparison["W"] / (comparison["W"] + comparison["L"])
    return comparison
