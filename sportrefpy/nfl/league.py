from datetime import datetime
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup

from sportrefpy.player.util.all_players import AllPlayers
from sportrefpy.league.league import League
from sportrefpy.util.enums import NumTeams
from sportrefpy.util.enums import SportEnum
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.formatter import Formatter


class NFL(League):
    def __init__(self):
        super().__init__()
        self._name = SportEnum.NFL.value
        self._num_teams = NumTeams.NFL
        self.url = SportURLs.NFL.value
        self.response = requests.get(f"{self.url}/teams")
        self.soup = BeautifulSoup(self.response.text, features="lxml")
        self.soup_attrs = {"data-stat": "team_name", "class": "left"}
        self.teams = self.get_teams()
        if datetime.today().month >= 9:
            self.current_season_year = datetime.today().year
        else:
            self.current_season_year = datetime.today().year - 1

    @staticmethod
    def players():
        return AllPlayers.nfl_players()

    def conference_standings(self, conf=None, season=None):
        """
        Season will be current year if it's not specified.
        """
        if not season:
            season = self.current_season_year

        # AFC
        afc = pd.read_html(f"{self.url}/years/{season}", attrs={"id": "AFC"})[0]
        afc.rename(columns={"Tm": "Team"}, inplace=True)
        afc["Team"] = afc["Team"].apply(lambda x: x.split("*")[0].strip())
        afc["Team"] = afc["Team"].apply(lambda x: x.split("+")[0].strip())
        afc = afc[~afc["W"].str.contains("AFC")]
        afc = afc.apply(pd.to_numeric, errors="ignore")
        afc.drop(columns={"SRS", "OSRS", "DSRS"}, inplace=True)
        afc.sort_values(["W", "SoS", "PF"], inplace=True, ascending=False)
        afc.reset_index(inplace=True, drop=True)
        afc.index = afc.index + 1

        # NFC
        nfc = pd.read_html(f"{self.url}/years/{season}", attrs={"id": "NFC"})[0]
        nfc.rename(columns={"Tm": "Team"}, inplace=True)
        nfc["Team"] = nfc["Team"].apply(lambda x: x.split("*")[0].strip())
        nfc["Team"] = nfc["Team"].apply(lambda x: x.split("+")[0].strip())
        nfc = nfc[~nfc["W"].str.contains("NFC")]
        nfc = nfc.apply(pd.to_numeric, errors="ignore")
        nfc.drop(columns={"SRS", "OSRS", "DSRS"}, inplace=True)
        nfc.sort_values(["W", "SoS", "PF"], inplace=True, ascending=False)
        nfc.reset_index(inplace=True, drop=True)
        nfc.index = nfc.index + 1

        if conf == "AFC":
            return Formatter.convert(afc, self.fmt)
        elif conf == "NFC":
            return Formatter.convert(nfc, self.fmt)
        return Formatter.convert(afc, self.fmt), Formatter.convert(nfc, self.fmt)

    def season_leaders(self, year=None):
        if year is None:
            season_leaders = {
                year: [None] for year in range(1966, datetime.today().year)
            }
            stats_leaders = []
            for year in range(1966, datetime.today().year):
                response = requests.get(f"{self.url}/years/{year}/")
                soup = BeautifulSoup(response.text, features="lxml")
                season_summary = soup.find_all("p")
                stats = [
                    stat.text.strip().replace(": ", ", ").split(", ")
                    for stat in season_summary
                    if stat.find("strong")
                ]
                stats = dict(
                    [stat[:2] for stat in stats if stat[0] != "Site Last Updated"]
                )
                if "League Champion" in stats.keys():
                    stats["Super Bowl Champion"] = stats.pop("League Champion")
                stats["Year"] = year
                stats_leaders.append(stats)
        season_leaders = pd.DataFrame(stats_leaders)
        season_leaders.set_index("Year", inplace=True)

        return Formatter.convert(season_leaders, self.fmt)

    @staticmethod
    def box_score(day, month, year, home_team):
        raise NotImplementedError

    def compare_franchises(self, franchises: List[str]):
        raise NotImplementedError

    def compare_players(self, players: List[str], total="career"):
        raise NotImplementedError
