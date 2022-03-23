import pytest
from sports_stats.nba.nba import NBAFranchise


def test_NBA_coach_playoffs():
    sixers = NBAFranchise('PHI')
    coaches = sixers.coaches_all_time_data()
    assert coaches.loc['Brett Brown', 'Playoffs'] == 3.0

def test_NBA_coach_winloss():
    warriors = NBAFranchise('GSW')
    coaches = warriors.coaches_all_time_data()
    assert coaches.loc['Don Nelson', 'W/L%'] == 0.488