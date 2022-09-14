from abc import ABC

import requests
from bs4 import BeautifulSoup
from bs4 import Tag
from requests import Response

from sportrefpy.errors.errors import PlayerNotFoundError
from sportrefpy.player.util.player_checker import PlayerChecker


class Player(ABC):
    def __init__(self, name: str, fmt: str = "dict"):
        self.sport_url = None
        self.name = name
        self.fmt = fmt
        if not PlayerChecker.is_valid_player(self.players, name):
            raise PlayerNotFoundError(name)

    @property
    def response(self) -> Response:
        return requests.get(f"{self.sport_url}/players/{self.identifying_letter}")

    @property
    def soup(self) -> Tag:
        return BeautifulSoup(self.response.text, features="lxml")

    def accolades(self):
        accolades = self.player_soup.find("ul", {"id": "bling"})
        if accolades:
            return {
                accolade.text.strip() for accolade in accolades if accolade.text.strip()
            }
        return None

    @property
    def identifying_letter(self):
        raise NotImplementedError

    @property
    def players(self):
        raise NotImplementedError

    @property
    def player_url(self):
        return self.players[self.name]
