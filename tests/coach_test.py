import pytest
from sportrefpy.nba.team import NBAFranchise
from sportrefpy.nhl.team import NHLFranchise
from sportrefpy.nfl.team import NFLFranchise
from sportrefpy.mlb.team import MLBFranchise


def test_NBA_coach_playoffs():
    sixers = NBAFranchise("PHI")
    coaches = sixers.coaches_all_time_data()
    assert coaches.loc["Brett Brown", "Playoffs"] == 3.0


def test_NBA_coach_winloss():
    warriors = NBAFranchise("GSW")
    coaches = warriors.coaches_all_time_data()
    assert coaches.loc["Don Nelson", "W/L%"] == 0.488


def test_nba_coach_exists():
    heat = NBAFranchise("MIA")
    coaches = heat.coaches_all_time_data()
    with pytest.raises(KeyError):
        coaches.loc["Pat Spoelstra"]


def test_NHL_coach():
    flyers = NHLFranchise("PHI")
    coaches = flyers.coaches_all_time_data()
    assert coaches.loc["Ken Hitchcock", "Playoff W-L%"] == 0.514


def test_NFL_coach():
    eagles = NFLFranchise("PHI")
    coaches = eagles.coaches_all_time_data()
    assert coaches.loc["Dick Vermeil", "W-L%"] == 0.535


def test_MLB_managers():
    reds = MLBFranchise("CIN")
    managers = reds.managers_all_time_stats()
    assert managers.loc["Buck Ewing", "W"] == 394
