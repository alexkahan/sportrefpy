import pandas as pd

from sports_stats.nba.player import NBAPlayer
from sports_stats.nba.team import NBAFranchise


def compare_players(players, stats, total='career'):
    '''
    Compare regular season, post season, and career totals between two players.
    '''

    players = [NBAPlayer(player) for player in players]
    if not stats:
        if total == 'career':
            comparison = pd.concat([player.career_totals() for player in players], axis=1)
            comparison.columns = [player.full_name for player in players]
        elif total == 'reg':
            comparison = pd.concat([player.regular_season_stats().sum() for player in players], axis=1)
            comparison.columns = [player.full_name for player in players]
            comparison.drop(index={'Age', 'Tm', 'Lg', 'Pos', 'FG%', '3P%', '2P%', 'eFG%', 'FT%'}, inplace=True)
        elif total == 'post':
            comparison = pd.concat([player.post_season_stats().sum() for player in players], axis=1)
            comparison.columns = [player.full_name for player in players]
            comparison.drop(index={'Age', 'Tm', 'Lg', 'Pos', 'FG%', '3P%', '2P%', 'eFG%', 'FT%'}, inplace=True)
    elif stats:
        if total == 'career':
            comparison = pd.concat([player.career_totals().loc[stats] for player in players], axis=1)
            comparison.columns = [player.full_name for player in players]
        elif total == 'reg':
            comparison = pd.concat([player.regular_season_stats().sum() for player in players], axis=1)
            comparison.columns = [player.full_name for player in players]
            comparison.drop(index={'Age', 'Tm', 'Lg', 'Pos', 'FG%', '3P%', '2P%', 'eFG%', 'FT%'}, inplace=True)
            comparison = comparison.loc[stats]
        elif total == 'post':
            comparison = pd.concat([player.post_season_stats().sum() for player in players], axis=1)
            comparison.columns = [player.full_name for player in players]
            comparison.drop(index={'Age', 'Tm', 'Lg', 'Pos', 'FG%', '3P%', '2P%', 'eFG%', 'FT%'}, inplace=True)
            comparison = comparison.loc[stats]
        # comparison['Diff'] = abs(comparison[player1] - comparison[player2])
        comparison = comparison.transpose()
        comparison.columns = [stats]
        return comparison
    else:
        raise Exception


def compare_franchises(teams):
    teams = [NBAFranchise(team) for team in teams]
    comparison = pd.concat([team.season_history()[['W', 'L']].sum() for team in teams], axis=1)
    comparison.columns = [team.franchise_name for team in teams]
    comparison = comparison.transpose()
    comparison['W%'] = comparison['W'] / (comparison['W'] + comparison['L'])
    return comparison