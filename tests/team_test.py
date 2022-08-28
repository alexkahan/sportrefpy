import pytest

from sportrefpy.nba.team import NBAFranchise
from sportrefpy.nba.analysis import compare_franchises as nba_compare_franchises
from sportrefpy.nhl.team import NHLFranchise
from sportrefpy.nfl.team import NFLFranchise
from sportrefpy.mlb.team import MLBFranchise
from sportrefpy.cfb.cfb import CFBSchool
from sportrefpy.nhl.analysis import compare_franchises as nhl_compare_franchises
from sportrefpy.mlb.analysis import compare_franchises as mlb_compare_franchises


def test_NBA_franchise():
    sixers = NBAFranchise("PhI")
    assert sixers.franchise_name == "Philadelphia 76ers"


def test_NBA_seasons():
    celtics = NBAFranchise("boS")
    seasons = celtics.season_history()
    assert seasons.loc["2011-12", "DRtg"] == 98.2


def test_NBA_franchise_comparison():
    comparison = nba_compare_franchises(["PHI", "CLE"])
    assert (
        comparison.loc["Philadelphia 76ers", "W"]
        > comparison.loc["Cleveland Cavaliers", "W"]
    )


def test_NHL_franchise():
    golden_knights = NHLFranchise("VEG")
    assert golden_knights.franchise_name == "Vegas Golden Knights"


def test_NHL_seasons():
    buffalo = NHLFranchise("BUF")
    seasons = buffalo.season_history()
    assert seasons.loc["1999-00", "Finish"] == "3rd of 5"


def test_NHL_roster():
    flyers = NHLFranchise("PHI")
    assert "Scott Laughton" in flyers.roster(2022).index


def test_NHL_goalies():
    hurricanes = NHLFranchise("CAR")
    goalies = hurricanes.goalies_all_time_stats()
    assert goalies.loc["Cam Ward", "SV"] == 17261


def test_NHL_skaters():
    penguins = NHLFranchise("PIT")
    skaters = penguins.skaters_all_time_stats()
    assert skaters.loc["Mario Lemieux", "G"] == 690


def test_NHL_franchise_comparison():
    comparison = nhl_compare_franchises(["TBL", "DET"])
    assert (
        comparison.loc["Tampa Bay Lightning", "W"]
        < comparison.loc["Detroit Red Wings", "W"]
    )


def test_NFL_franchise():
    kc = NFLFranchise("kan")
    assert kc.franchise_name == "Kansas City Chiefs"


def test_NFL_seasons():
    eagles = NFLFranchise("PHI")
    seasons = eagles.season_history()
    assert seasons.loc[2017, "Playoffs"] == "Won SB"


def test_NFL_coaching():
    jets = NFLFranchise("nyj")
    coaches = jets.coaches_all_time_data()
    assert "Rex Ryan" in coaches.index


def test_MLB_franchise():
    dodgers = MLBFranchise("LAD")
    assert dodgers.franchise_name == "Los Angeles Dodgers"


def test_MLB_seasons():
    nyy = MLBFranchise("NYY")
    seasons = nyy.season_history()
    assert seasons.loc[1921, "Playoffs"] == "Lost WS (5-3)"


def test_MLB_roster():
    braves = MLBFranchise("ATL")
    roster = braves.roster(1995)
    assert "Chipper Jones" in roster.index


def test_MLB_batters():
    dodgers = MLBFranchise("LAD")
    batters = dodgers.batters_all_time_stats()
    assert batters.loc["Jackie Robinson", "G"] == 1382


def test_MLB_pitchers():
    pirates = MLBFranchise("PIT")
    pitchers = pirates.pitchers_all_time_stats()
    assert pitchers.loc["Jim Bunning", "L"] == 23


def compare_MLB_franchise():
    comparison = mlb_compare_franchises(["PHI", "DET"])
    assert (
        comparison.loc["Philadelphia Phillies", "L"]
        > comparison.loc["Detroit Tigers", "L"]
    )


def test_CBB_school():
    af = CBBSchool("air-force")
    assert af.school == "Air Force Falcons"


def test_CFB_school():
    wake = CFBSchool("wake-forest")
    assert wake.school == "Wake Forest"
