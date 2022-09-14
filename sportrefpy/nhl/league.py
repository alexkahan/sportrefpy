import pandas as pd
import requests
from bs4 import BeautifulSoup

from sportrefpy.player.util.all_players import AllPlayers
from sportrefpy.league.league import League
from sportrefpy.util.enums import NumTeams
from sportrefpy.util.enums import SportEnum
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.formatter import Formatter


class NHL(League):
    def __init__(self):
        super().__init__()
        self._name = SportEnum.NHL.value
        self._num_teams = NumTeams.NHL
        self.url = SportURLs.NHL.value
        self.standings_url = f"{self.url}/boxscores/"
        self.response = requests.get(f"{self.url}/teams")
        self.soup = BeautifulSoup(self.response.text, features="lxml")
        self.soup_attrs = {"data-stat": "franch_name"}
        self.teams = self.get_teams()

    @staticmethod
    def players():
        return AllPlayers.nhl_players()

    def conference_standings(self, conf=None):
        # Eastern Conference
        east_conf = pd.read_html(self.standings_url)[-2]
        east_conf.rename(columns={"Unnamed: 0": "Team"}, inplace=True)
        east_conf = east_conf[~east_conf["Team"].str.contains("Division")]
        east_conf = east_conf.apply(pd.to_numeric, errors="ignore")
        east_conf.sort_values(["PTS", "RgPt%", "GF"], inplace=True, ascending=False)
        east_conf.reset_index(inplace=True, drop=True)
        east_conf.index = east_conf.index + 1

        # Western Conference
        west_conf = pd.read_html(self.standings_url)[-1]
        west_conf.rename(columns={"Unnamed: 0": "Team"}, inplace=True)
        west_conf = west_conf[~west_conf["Team"].str.contains("Division")]
        west_conf = west_conf.apply(pd.to_numeric, errors="ignore")
        west_conf.sort_values(["PTS", "RgPt%", "GF"], inplace=True, ascending=False)
        west_conf.reset_index(inplace=True, drop=True)
        west_conf.index = west_conf.index + 1

        if conf == "east":
            return Formatter.convert(east_conf, self.fmt)
        elif conf == "west":
            return Formatter.convert(west_conf, self.fmt)
        return Formatter.convert(east_conf, self.fmt), Formatter.convert(
            west_conf, self.fmt
        )
