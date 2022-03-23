import pytest
from sports_stats.nba import NBA, NBAFranchise
from sports_stats.nhl import NHL, NHLFranchise
from sports_stats.nfl import NFL, NFLFranchise
from sports_stats.mlb import MLB, MLBFranchise
from sports_stats.cbb import CBB, CBBSchool
from sports_stats.cfb import CFB, CFBSchool

def test_NBA():
    nba = NBA()
    assert len(nba.teams) == 30

def test_NBA_franchise():
    sixers = NBAFranchise('PHI')
    assert sixers.franchise == "Philadelphia 76ers"


def test_NHL():
    nhl = NHL()
    assert len(nhl.teams) == 32

def test_NHL_franchise():
    golden_knights = NHLFranchise('VEG')
    assert golden_knights.franchise == "Vegas Golden Knights"


def test_NFL():
    nfl = NFL()
    assert len(nfl.teams) == 32

def test_NFL_franchise():
    kc = NFLFranchise('kan')
    assert kc.franchise == "Kansas City Chiefs"


def test_MLB():
    mlb = MLB()
    assert len(mlb.teams) == 30

def test_MLB_franchise():
    dodgers = MLBFranchise('LAD')
    assert dodgers.franchise == "Los Angeles Dodgers"


def test_CBB():
    cbb = CBB()
    assert len(cbb.schools) == 485

def test_CBB_school():
    af = CBBSchool('air-force')
    assert af.school == "Air Force Falcons"


def test_CFB():
    cfb = CFB()
    assert len(cfb.schools) == 298

def test_CFB_school():
    wake = CFBSchool('wake-forest')
    assert wake.school == "Wake Forest"