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
