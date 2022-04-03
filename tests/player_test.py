import pytest
import numpy as np

from sportrefpy.nba.team import NBAFranchise
from sportrefpy.nba.player import NBAPlayer
from sportrefpy.nba.analysis import compare_players
from sportrefpy.nhl.team import NHLFranchise
from sportrefpy.mlb.team import MLBFranchise

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
    players = clippers.roster(2022)
    assert 'Kawhi Leonard' in players.index

def test_NBA_player_regular_season_stats():
    the_answer = NBAPlayer('Allen Iverson')
    assert the_answer.regular_season_stats().loc['1997-98', 'PTS'] == 1758.0

def test_NBA_player_post_season_stats_false():
    fo = NBAPlayer('Frank Oleynick')
    assert fo.playoffs is False and fo.post_season_stats() is None

def test_NBA_player_post_season_stats_true():
    sheed = NBAPlayer('Rasheed Wallace')
    assert sheed.post_season_stats().loc['2009-10', 'PTS'] == 147.0

def test_NBA_player_reg_season_game_log():
    kg = NBAPlayer('Kevin Garnett')
    gl = kg.reg_season_game_log('1999-00')
    assert gl.loc[2, 'FG'] == 13.0

def test_NBA_player_post_season_game_log():
    dametime = NBAPlayer('Damian Lillard')
    gl = dametime.post_season_game_log()
    assert np.isnan(gl.loc[56, 'FG'])

def test_NBA_player_comparison():
    comparison = compare_players(["Shaquille O'Neal", "Kobe Bryant"], stats=['PTS'])
    assert comparison.sum()['PTS'] == 73961.0


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
    players = panthers.roster()
    assert 'Aleksander Barkov' in players.index

def test_NHL_seasons():
    redwings = NHLFranchise('DET')
    seasons = redwings.season_history('2012-13')
    assert seasons.loc['W'] == 24


def test_MLB_batter():
    sea = MLBFranchise('SEA')
    batters = sea.batters_all_time_stats()
    assert batters.loc['Ken Griffey Jr.', 'PA'] == 7250.0

def test_MLB_pitcher():
    bos = MLBFranchise('BOS')
    pitchers = bos.pitchers_all_time_stats()
    assert pitchers.loc['Dennis Eckersley', 'To'] == 1998
