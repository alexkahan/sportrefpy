import csv
import os

import pandas as pd
import requests

from sportrefpy.nhl.league import NHL
from sportrefpy.player.player import Player
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.player_dictionary import PlayerDictionary


class NHLPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        if not self.is_valid_player:
            PlayerDictionary.make_suggestion(NHL().player_dict, name)
        self.full_name: str = name

    @property
    def identifying_letter(self):
        return self.name.split()[-1][0].lower()

    @property
    def players(self):
        with open(
            (os.path.dirname(os.path.dirname(__file__)) + "/assets/nhl_players.txt"),
            newline="",
        ) as players:
            player_reader = csv.reader(players)
            return [player[0] for player in player_reader]

    @property
    def player_url(self):
        for item in self.soup.find_all("p", attrs={"class": "nhl"}):
            if self.name in item.text.split(" (")[0]:
                return f"{SportURLs.NHL.value}{item.find('a')['href']}"

    @property
    def response(self):
        return requests.get(f"{SportURLs.NHL.value}/players/{self.identifying_letter}")

    @property
    def is_valid_player(self):
        return self.name in self.players

    def regular_season_stats(self):
        """
        Returns a players regular seasons stats by season or by career.

        It can show stats per year in total or by team,
        if they played for multiple.
        """

        stats = pd.read_html(self.player_url, header=[1])[0]
        stats.columns = [
            "Season",
            "Age",
            "Tm",
            "Lg",
            "GP",
            "G",
            "A",
            "PTS",
            "+/-",
            "PIM",
            "EVG",
            "PPG",
            "SHG",
            "GWG",
            "EVA",
            "PPA",
            "SHA",
            "S",
            "S%",
            "TOI",
            "ATOI",
            "Awards",
        ]
        stats = stats[~stats["Season"].str.contains("season|Career|yr|yrs")]
        stats.set_index("Season", inplace=True)
        stats = stats[stats["Lg"] == "NHL"]
        stats.drop(columns={"Lg", "TOI", "ATOI"}, inplace=True)

        return stats
