import pytest
from sports_stats.nba.team import NBAFranchise
from sports_stats.nhl.team import NHLFranchise

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


def test_NHL_goalie():
    bruins = NHLFranchise('BOS')
    goalies = bruins.goalies_all_time_stats()
    assert goalies.loc['Gerry Cheevers', 'SV'] == 10579.0

def test_NHL_skaters():
    veg = NHLFranchise('VEG')
    skaters = veg.skaters_all_time_stats()
    assert skaters.loc['Pierre-Edouard Bellemare', 'PPG'] == 0.0


def test_NHL_player():
    panthers = NHLFranchise('FLA')
    players = panthers.current_roster()
    assert 'Aleksander Barkov' in players.index