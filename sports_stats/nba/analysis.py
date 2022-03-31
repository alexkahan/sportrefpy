from sports_stats.nba.player import NBAPlayer

import pandas as pd

def compare_players(player1, player2, stat=None, total='career'):
    '''
    Compare regular season, post season, and career totals between two players.
    '''

    p1 = NBAPlayer(player1)
    p2 = NBAPlayer(player2)
    if not stat:
        if total == 'career':
            comparison = pd.concat([p1.career_totals(), p2.career_totals()], axis=1)
            comparison.columns = [player1, player2]
        elif total == 'reg':
            comparison = pd.concat([p1.regular_season_stats().sum(), p2.regular_season_stats().sum()], axis=1)
            comparison.columns = [player1, player2]
            comparison.drop(index={'Age', 'Tm', 'Lg', 'Pos', 'FG%', '3P%', '2P%', 'eFG%', 'FT%'}, inplace=True)
        elif total == 'post':
            comparison = pd.concat([p1.post_season_stats().sum(), p2.post_season_stats().sum()], axis=1)
            comparison.columns = [player1, player2]
            comparison.drop(index={'Age', 'Tm', 'Lg', 'Pos', 'FG%', '3P%', '2P%', 'eFG%', 'FT%'}, inplace=True)
    elif stat:
        if total == 'career':
            comparison = pd.concat([p1.career_totals().loc[stat], p2.career_totals().loc[stat]], axis=1)
            comparison.columns = [player1, player2]
        elif total == 'reg':
            comparison = pd.concat([p1.regular_season_stats().sum(), p2.regular_season_stats().sum()], axis=1)
            comparison.columns = [player1, player2]
            comparison.drop(index={'Age', 'Tm', 'Lg', 'Pos', 'FG%', '3P%', '2P%', 'eFG%', 'FT%'}, inplace=True)
            comparison = comparison.loc[stat]
        elif total == 'post':
            comparison = pd.concat([p1.post_season_stats().sum(), p2.post_season_stats().sum()], axis=1)
            comparison.columns = [player1, player2]
            comparison.drop(index={'Age', 'Tm', 'Lg', 'Pos', 'FG%', '3P%', '2P%', 'eFG%', 'FT%'}, inplace=True)
            comparison = comparison.loc[stat]
        comparison['Diff'] = abs(comparison[player1] - comparison[player2])
        return comparison
    else:
        raise Exception