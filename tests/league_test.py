import pytest
from sportrefpy.nba.league import NBA
from sportrefpy.nhl.league import NHL
from sportrefpy.nfl.league import NFL
from sportrefpy.mlb.league import MLB
from sportrefpy.cbb.cbb import CBB
from sportrefpy.cfb.cfb import CFB

def test_NBA():
    nba = NBA()
    assert len(nba.teams) == 30

def test_NBA_standings():
    nba = NBA()
    assert len(nba.conference_standings('east')) == 15 and \
        len(nba.conference_standings('west')) == 15


def test_NHL():
    nhl = NHL()
    assert len(nhl.teams) == 32

def test_NHL_standings():
    nhl = NHL()
    assert len(nhl.conference_standings('east')) == 16 and \
        len(nhl.conference_standings('west')) == 16


def test_NFL():
    nfl = NFL()
    assert len(nfl.teams) == 32


def test_MLB():
    mlb = MLB()
    assert len(mlb.teams) == 30

def test_MLB_standings():
    mlb = MLB()
    standings = mlb.standings(2020)
    assert standings.loc[1, 'Team'] == 'Los Angeles Dodgers'


def test_CBB():
    cbb = CBB()
    assert len(cbb.schools) == 485


def test_CFB():
    cfb = CFB()
    assert len(cfb.schools) == 298