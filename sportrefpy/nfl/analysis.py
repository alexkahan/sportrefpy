import pandas as pd

# from sportrefpy.nfl.player import NFLPlayer
from sportrefpy.nfl.team import NFLFranchise


def compare_franchises(teams):
    teams = [NFLFranchise(team) for team in teams]
    comparison = pd.concat([team.season_history()[['W', 'L', 'T']].sum() for team in teams], axis=1)
    comparison.columns = [team.franchise_name for team in teams]
    comparison = comparison.transpose()
    comparison['W%'] = comparison['W'] / (comparison['W'] + comparison['L'])
    return comparison