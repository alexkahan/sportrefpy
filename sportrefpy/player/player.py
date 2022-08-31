from abc import ABC

from bs4 import BeautifulSoup


class Player(ABC):
    def __init__(self, name: str):
        self.name = name

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
