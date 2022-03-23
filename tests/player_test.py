import pytest
from sports_stats.nba import NBAFranchise
# from sports_stats.nhl import NHL, NHLFranchise
# from sports_stats.nfl import NFL, NFLFranchise
# from sports_stats.mlb import MLB, MLBFranchise
# from sports_stats.cbb import CBB, CBBSchool
# from sports_stats.cfb import CFB, CFBSchool

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