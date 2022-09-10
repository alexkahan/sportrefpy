import os

import enchant
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests import Response

from sportrefpy.player.player import Player
from sportrefpy.player.util.all_players import AllPlayers
from sportrefpy.util.enums import SportURLs


class CBBPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.full_name: str = name
        self.sport_url = SportURLs.CBB.value

    @property
    def identifying_letter(self):
        return self.name.split()[-1][0].lower()

    @property
    def player_response(self) -> Response:
        return requests.get(self.player_url)

    @property
    def player_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.player_response.text, features="lxml")

    #         player_dict = enchant.PyPWL(
    #             os.path.dirname(os.path.dirname(__file__)) + "\\assets\\cbb_players.txt"
    #         )
    #         first_letter_last_name = player.split()[-1][0].lower()
    #         with open(
    #             os.path.dirname(os.path.dirname(__file__)) + "\\assets\\cbb_players.txt",
    #             "r",
    #         ) as player_dict:
    #             if player in player_dict.read():
    #                 response = requests.get(
    #                     f"{self.url}/cbb/players/{first_letter_last_name}-index.html"
    #                 )
    #                 soup = BeautifulSoup(response.text, features="lxml")
    #                 for item in soup.find_all("p"):
    #                     if player in item.text.split(" (")[0]:
    #                         self.player_url = self.url + item.find("a")["href"]
    #                         self.full_name = player
    #             else:
    #                 try:
    #                     suggestion = player_dict.suggest(player)[0]
    #                     message = f"""<{player}> not found.
    # Is it possible you meant {suggestion}?
    # Player names are case-sensitive."""
    #                 except:
    #                     message = f"""<{player}> not found.
    # Player names are case-sensitive."""
    #                 raise PlayerNotFound(message)

    @property
    def players(self) -> dict:
        return AllPlayers.cbb_players()

    def stats_totals(self, stat=None):
        """
        Returns totals of all of a players stats
        """
        if stat is None:
            stats = pd.read_html(self.player_url, attrs={"id": "players_totals"})[0]
            stats = stats[~stats["Season"].str.contains("Career")]
            stats = stats.apply(pd.to_numeric, errors="ignore")
            stats.set_index("Season", inplace=True)

        return stats
