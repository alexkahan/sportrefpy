import pandas as pd

from sportrefpy.mlb.player import MLBPlayer
from sportrefpy.mlb.team import MLBFranchise


def compare_franchises(teams):
    teams = [MLBFranchise(team) for team in teams]
    comparison = pd.concat([team.season_history()[['W', 'L', 'Ties']].sum() for team in teams], axis=1)
    comparison.columns = [team.franchise_name for team in teams]
    comparison = comparison.transpose()
    comparison['W%'] = comparison['W'] / (comparison['W'] + comparison['L'])
    return comparison