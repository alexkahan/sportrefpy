from abc import ABC
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4 import Tag
from requests import Response

from sportrefpy.errors.errors import PlayerNotFoundError
from sportrefpy.util.player_checker import PlayerChecker


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

    @property
    def identifying_letter(self):
        raise NotImplementedError

    @property
    def players(self):
        raise NotImplementedError

    @property
    def player_url(self):
        raise NotImplementedError

    @property
    def is_valid_player(self):
        raise NotImplementedError

    @classmethod
    def compare(cls, players: List[str], **kwargs):
        raise NotImplementedError
