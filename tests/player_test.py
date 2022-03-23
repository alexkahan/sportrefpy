import pytest
from sports_stats.nba.nba import NBAFranchise


def test_NBA_player_FGA():
    sixers = NBAFranchise('PHI')
    players = sixers.players_all_time_stats()
    assert players.loc['James Young', 'FGA'] == 14.0

def test_NBA_player_TRB():
    warriors = NBAFranchise('GSW')
    players = warriors.players_all_time_stats()
    assert players.loc['Wilt Chamberlain', 'TRB'] == 10768.0

def test_NBA_player():
    clippers = NBAFranchise('LAC')
    players = clippers.current_roster()
    assert 'Kawhi Leonard' in players.index