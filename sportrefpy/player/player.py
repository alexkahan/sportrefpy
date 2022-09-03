from abc import ABC
from typing import List

from bs4 import BeautifulSoup


class Player(ABC):
    def __init__(self, name: str, fmt: str = "dict"):
        self.name = name
        self.fmt = fmt

    @property
    def soup(self):
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
