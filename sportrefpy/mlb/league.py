from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4 import Comment

from sportrefpy.player.util.all_players import AllPlayers
from sportrefpy.sport.sport import Sport
from sportrefpy.util.enums import NumTeams
from sportrefpy.util.enums import SportEnum
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.formatter import Formatter


class MLB(Sport):
    def __init__(self):
        super().__init__()
        self._name = SportEnum.MLB.value
        self._num_teams = NumTeams.MLB
        self.url = SportURLs.MLB.value
        self.response = requests.get(f"{self.url}/teams")
        self.soup = BeautifulSoup(self.response.text, features="lxml")
        self.soup_attrs = {"data-stat": "franchise_name"}
        self.teams = self.get_teams()
        if datetime.today().month >= 4:
            self.current_season_year = datetime.today().year
        else:
            self.current_season_year = datetime.today().year - 1

    def get_season(self, season):
        if not season:
            return self.current_season_year
        return season

    @staticmethod
    def players():
        return AllPlayers.mlb_players()

    def standings(self, season=None):
        """
        Season will be current year if it's not specified. Overall standings.
        """
        season = self.get_season(season)

        page = requests.get(f"{self.url}/leagues/majors/{str(season)}-standings.shtml")
        soup = BeautifulSoup(page.text, "html.parser")

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        tables = []
        for comment in comments:
            if "table" in str(comment):
                try:
                    tables.append(pd.read_html(str(comment)))
                except:
                    continue
        standings = tables[-1][0]
        standings.dropna(axis="rows", how="any", inplace=True)
        standings.rename(columns={"Tm": "Team"}, inplace=True)
        standings.drop(columns={"Rk"}, inplace=True)
        standings.index = standings.index + 1

        return Formatter.convert(standings, self.fmt)

    def al_standings(self, season=None):

        season = self.get_season(season)

        page = requests.get(f"{self.url}/leagues/AL/{str(season)}-standings.shtml").text
        soup = BeautifulSoup(page, "html.parser")

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        tables = []
        for comment in comments:
            if "table" in str(comment):
                try:
                    tables.append(pd.read_html(str(comment)))
                except:
                    continue
        standings = tables[4][0]
        standings.dropna(axis="rows", how="any", inplace=True)
        standings.rename(columns={"Tm": "Team"}, inplace=True)
        standings.drop(columns={"Rk"}, inplace=True)
        standings.index = standings.index + 1

        return Formatter.convert(standings, self.fmt)

    def nl_standings(self, season=None):

        season = self.get_season(season)

        page = requests.get(f"{self.url}/leagues/NL/{str(season)}-standings.shtml").text
        soup = BeautifulSoup(page, "html.parser")

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        tables = []
        for comment in comments:
            if "table" in str(comment):
                try:
                    tables.append(pd.read_html(str(comment)))
                except:
                    continue
        standings = tables[4][0]
        standings.dropna(axis="rows", how="any", inplace=True)
        standings.rename(columns={"Tm": "Team"}, inplace=True)
        standings.drop(columns={"Rk"}, inplace=True)
        standings.index = standings.index + 1

        return Formatter.convert(standings, self.fmt)

    @staticmethod
    def box_score(day, month, year, home_team):
        raise NotImplementedError
