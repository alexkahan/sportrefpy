import pandas as pd

from sportrefpy.nhl.team import NHLTeam


def compare_franchises(teams):
    teams = [NHLTeam(team) for team in teams]
    comparison = pd.concat(
        [team.season_history()[["W", "L"]].sum() for team in teams], axis=1
    )
    comparison.columns = [team.franchise_name for team in teams]
    comparison = comparison.transpose()
    comparison["W%"] = comparison["W"] / (comparison["W"] + comparison["L"])
    return comparison
