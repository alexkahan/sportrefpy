import requests
from bs4 import BeautifulSoup
from requests import Response

from sportrefpy.nfl.league import NFL
from sportrefpy.player.player import Player
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.player_dictionary import PlayerDictionary


class NFLPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        if not self.is_valid_player:
            PlayerDictionary.make_suggestion(NFL().player_dict, name)
        self.full_name: str = name

    @property
    def identifying_letter(self):
        return self.name.split()[1][0].upper()

    @property
    def players(self):
        return self.soup.find("div", attrs={"id": "div_players"})

    @property
    def player_url(self):
        for player in self.players:
            if self.name in player.text:
                return f"{SportURLs.NFL.value}{player.find('a')['href']}"

    @property
    def response(self) -> Response:
        return requests.get(f"{SportURLs.NFL.value}/players/{self.identifying_letter}")

    @property
    def player_response(self) -> Response:
        raise NotImplementedError

    @property
    def player_soup(self) -> BeautifulSoup:
        raise NotImplementedError

    @property
    def is_valid_player(self):
        return self.name in self.players.text
