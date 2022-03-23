import pytest
from sports_stats.nba.league import NBA
from sports_stats.nhl.league import NHL
from sports_stats.nfl.league import NFL
from sports_stats.mlb.league import MLB
from sports_stats.cbb.cbb import CBB
from sports_stats.cfb.cfb import CFB

def test_NBA():
    nba = NBA()
    assert len(nba.teams) == 30


def test_NHL():
    nhl = NHL()
    assert len(nhl.teams) == 32


def test_NFL():
    nfl = NFL()
    assert len(nfl.teams) == 32


def test_MLB():
    mlb = MLB()
    assert len(mlb.teams) == 30


def test_CBB():
    cbb = CBB()
    assert len(cbb.schools) == 485


def test_CFB():
    cfb = CFB()
    assert len(cfb.schools) == 298