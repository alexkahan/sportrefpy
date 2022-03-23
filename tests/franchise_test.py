import pytest
from sports_stats.nba import NBAFranchise
from sports_stats.nhl import NHLFranchise
from sports_stats.nfl import NFLFranchise
from sports_stats.mlb import MLBFranchise

def test_NBA():
    sixers = NBAFranchise('PHI')
    assert sixers.franchise == "Philadelphia 76ers"

def test_NHL():
    golden_knights = NHLFranchise('VEG')
    assert golden_knights.franchise == "Vegas Golden Knights"

def test_NFL():
    kc = NFLFranchise('kan')
    assert kc.franchise == "Kansas City Chiefs"

def test_MLB():
    dodgers = MLBFranchise('LAD')
    assert dodgers.franchise == "Los Angeles Dodgers"