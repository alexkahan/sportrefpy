import pandas as pd
import requests
from bs4 import BeautifulSoup

from sportrefpy.sport.sport import Sport
from sportrefpy.util.enums import NumTeams
from sportrefpy.util.enums import SportEnum
from sportrefpy.util.enums import SportURLs


class NBA(Sport):
    def __init__(self):
        super().__init__()
        self._name = SportEnum.NBA.value
        self._num_teams = NumTeams.NBA
        self.url = SportURLs.NBA.value
        self.standings_url = f"{self.url}/boxscores/"
        self.response = requests.get(f"{self.url}/teams")
        self.soup = BeautifulSoup(self.response.text, features="lxml")
        self.soup_attrs = {"data-stat": "franch_name"}
        self.teams = self.get_teams()

    def conference_standings(self, conf=None):
        east_conf = pd.read_html(self.standings_url)[-2]
        east_conf.index = east_conf.index + 1
        east_conf.replace("—", 0, inplace=True)
        east_conf["GB"] = pd.to_numeric(east_conf["GB"])

        west_conf = pd.read_html(self.standings_url)[-1]
        west_conf.index = west_conf.index + 1
        west_conf.replace("—", 0, inplace=True)
        west_conf["GB"] = pd.to_numeric(west_conf["GB"])

        if conf == "east":
            return east_conf
        elif conf == "west":
            return west_conf

        return east_conf, west_conf
