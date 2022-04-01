import pytest

from sports_stats.nba.team import NBAFranchise
from sports_stats.nba.analysis import compare_franchises
from sports_stats.nhl.team import NHLFranchise
from sports_stats.nfl.team import NFLFranchise
from sports_stats.mlb.team import MLBFranchise
from sports_stats.cbb.cbb import CBBSchool
from sports_stats.cfb.cfb import CFBSchool


def test_NBA_franchise():
    sixers = NBAFranchise('PhI')
    assert sixers.franchise_name == "Philadelphia 76ers"

def test_NBA_seasons():
    celtics = NBAFranchise('boS')
    seasons = celtics.season_history()
    assert seasons.loc['2011-12', 'DRtg'] == 98.2

def test_NBA_franchise_comparison():
    comparison = compare_franchises(['PHI', 'CLE'])
    assert comparison.loc['Philadelphia 76ers', 'W'] > comparison.loc['Cleveland Cavaliers', 'W']


def test_NHL_franchise():
    golden_knights = NHLFranchise('VEG')
    assert golden_knights.franchise == "Vegas Golden Knights"

def test_NHL_seasons():
    buffalo = NHLFranchise('BUF')
    seasons = buffalo.season_history()
    assert seasons.loc['1999-00', 'Finish'] == '3rd of 5'


def test_NFL_franchise():
    kc = NFLFranchise('kan')
    assert kc.franchise == "Kansas City Chiefs"

def test_NFL_seasons():
    eagles = NFLFranchise('PHI')
    seasons = eagles.season_history()
    assert seasons.loc[2017, 'Playoffs'] == 'Won SB'


def test_MLB_franchise():
    dodgers = MLBFranchise('LAD')
    assert dodgers.franchise == "Los Angeles Dodgers"

def test_MLB_seasons():
    nyy = MLBFranchise('NYY')
    seasons = nyy.season_history()
    assert seasons.loc[1921, 'Playoffs'] == 'Lost WS (5-3)'


def test_CBB_school():
    af = CBBSchool('air-force')
    assert af.school == "Air Force Falcons"


def test_CFB_school():
    wake = CFBSchool('wake-forest')
    assert wake.school == "Wake Forest"