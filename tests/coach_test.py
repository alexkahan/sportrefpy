import pytest
from sports_stats.nba import NBAFranchise
# from sports_stats.nhl import NHL, NHLFranchise
# from sports_stats.nfl import NFL, NFLFranchise
# from sports_stats.mlb import MLB, MLBFranchise
# from sports_stats.cbb import CBB, CBBSchool
# from sports_stats.cfb import CFB, CFBSchool

def test_NBA_coach_playoffs():
    sixers = NBAFranchise('PHI')
    coaches = sixers.coaches_all_time_data()
    assert coaches.loc['Brett Brown', 'Playoffs'] == 3.0

def test_NBA_coach_winloss():
    warriors = NBAFranchise('GSW')
    coaches = warriors.coaches_all_time_data()
    assert coaches.loc['Don Nelson', 'W/L%'] == 0.488