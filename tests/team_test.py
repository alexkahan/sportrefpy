import pytest
from sports_stats.nba.team import NBAFranchise
from sports_stats.nhl.team import NHLFranchise
from sports_stats.nfl.team import NFLFranchise
from sports_stats.mlb.team import MLBFranchise
from sports_stats.cbb.cbb import CBBSchool
from sports_stats.cfb.cfb import CFBSchool


def test_NBA_franchise():
    sixers = NBAFranchise('PHI')
    assert sixers.franchise == "Philadelphia 76ers"


def test_NHL_franchise():
    golden_knights = NHLFranchise('VEG')
    assert golden_knights.franchise == "Vegas Golden Knights"


def test_NFL_franchise():
    kc = NFLFranchise('kan')
    assert kc.franchise == "Kansas City Chiefs"


def test_MLB_franchise():
    dodgers = MLBFranchise('LAD')
    assert dodgers.franchise == "Los Angeles Dodgers"


def test_CBB_school():
    af = CBBSchool('air-force')
    assert af.school == "Air Force Falcons"


def test_CFB_school():
    wake = CFBSchool('wake-forest')
    assert wake.school == "Wake Forest"