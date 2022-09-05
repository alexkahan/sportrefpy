import requests
from bs4 import BeautifulSoup
from requests import Response

from sportrefpy.nfl.league import NFL
from sportrefpy.player.player import Player
from sportrefpy.util.all_players import AllPlayers
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.player_checker import PlayerChecker


class NFLPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.full_name: str = name
        self.sport_url = SportURLs.NFL.value

    @property
    def identifying_letter(self):
        return self.name.split()[1][0].upper()

    @property
    def players(self) -> set:
        return AllPlayers.nfl_players()

    @property
    def player_url(self):
        for player in self.players:
            if self.name in player.text:
                return f"{SportURLs.NFL.value}{player.find('a')['href']}"

    @property
    def player_response(self) -> Response:
        raise NotImplementedError

    @property
    def player_soup(self) -> BeautifulSoup:
        raise NotImplementedError

    @property
    def is_valid_player(self):
        return self.name in self.players.text
