import requests
from datetime import datetime
from bs4 import BeautifulSoup, Comment
import pandas as pd

from sportrefpy.enums import SportURLs, NumTeams
from sportrefpy.league.league import League


class MLB(League):
    def __init__(self):
        super().__init__()
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

    def standings(self, season=None):
        """
        Season will be current year if it's not specified. Overall standings.
        """

        if season is None:
            season = self.current_season_year

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

        return standings

    def al_standings(self, season=None):

        if season is None:
            season = self.current_season_year

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

        return standings

    def nl_standings(self, season=None):

        if season is None:
            season = self.current_season_year

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

        return standings
