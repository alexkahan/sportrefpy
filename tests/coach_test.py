import pytest
from sports_stats.nba.team import NBAFranchise
from sports_stats.nhl.team import NHLFranchise
from sports_stats.nfl.team import NFLFranchise
from sports_stats.mlb.team import MLBFranchise


def test_NBA_coach_playoffs():
    sixers = NBAFranchise('PHI')
    coaches = sixers.coaches_all_time_data()
    assert coaches.loc['Brett Brown', 'Playoffs'] == 3.0

def test_NBA_coach_winloss():
    warriors = NBAFranchise('GSW')
    coaches = warriors.coaches_all_time_data()
    assert coaches.loc['Don Nelson', 'W/L%'] == 0.488

def test_nba_coach_exists():
    heat = NBAFranchise('MIA')
    coaches = heat.coaches_all_time_data()
    with pytest.raises(KeyError): 
        coaches.loc['Pat Spoelstra']

def test_NHL_coach():
    flyers = NHLFranchise('PHI')
    coaches = flyers.coaches_all_time_data()
    assert coaches.loc['Ken Hitchcock', 'Playoff W-L%'] == 0.514


def test_NFL_coach():
    eagles = NFLFranchise('PHI')
    coaches = eagles.coaches_all_time_data()
    assert coaches.loc['Dick Vermeil', 'W-L%'] == 0.535


def test_MLB_manager():
    nym = MLBFranchise('NYM')
    managers = nym.managers_all_time_data()
    assert managers.loc['Gil Hodges', 'BestFin'] == 1