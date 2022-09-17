import pytest

from sportrefpy.mlb.team import MLBTeam
from sportrefpy.nba.team import NBATeam
from sportrefpy.nfl.team import NFLTeam
from sportrefpy.nhl.team import NHLTeam


def test_NBA_coach_playoffs():
    sixers = NBATeam("PHI")
    coaches = sixers.coaches_all_time_data()
    assert coaches.loc["Brett Brown", "Playoffs"] == 3.0


def test_NBA_coach_winloss():
    warriors = NBATeam("GSW")
    coaches = warriors.coaches_all_time_data()
    assert coaches.loc["Don Nelson", "W/L%"] == 0.488


def test_nba_coach_exists():
    heat = NBATeam("MIA")
    coaches = heat.coaches_all_time_data()
    with pytest.raises(KeyError):
        coaches.loc["Pat Spoelstra"]


def test_NHL_coach():
    flyers = NHLTeam("PHI")
    coaches = flyers.coaches_all_time_data()
    assert coaches.loc["Ken Hitchcock", "Playoff W-L%"] == 0.514


def test_NFL_coach():
    eagles = NFLTeam("PHI")
    coaches = eagles.coaches_all_time_data()
    assert coaches.loc["Dick Vermeil", "W-L%"] == 0.535


def test_MLB_managers():
    reds = MLBTeam("CIN")
    managers = reds.managers_all_time_stats()
    assert managers.loc["Buck Ewing", "W"] == 394
