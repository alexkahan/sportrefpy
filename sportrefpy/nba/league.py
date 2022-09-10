from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup

from sportrefpy.nba.player import NBAPlayer
from sportrefpy.player.util.all_players import AllPlayers
from sportrefpy.sport.sport import Sport
from sportrefpy.sport.util.box_score import NBABoxScore
from sportrefpy.util.enums import NumTeams
from sportrefpy.util.enums import SportEnum
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.formatter import Formatter


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

    @staticmethod
    def players():
        return AllPlayers.nba_players()

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

    def compare_players(self, players: List[str], total="career"):
        players_to_compare = [NBAPlayer(player) for player in players]
        if total == "career":
            comparison = {
                player.name: player.career_totals() for player in players_to_compare
            }
        elif total == "reg":
            comparison = {
                player.name: player.regular_season_stats()
                for player in players_to_compare
            }
        elif total == "post":
            comparison = {
                player.name: player.post_season_stats() for player in players_to_compare
            }
        return Formatter.convert(comparison, self.fmt)

    @staticmethod
    def box_score(day, month, year, home_team):
        return NBABoxScore.exact_game(day, month, year, home_team)
