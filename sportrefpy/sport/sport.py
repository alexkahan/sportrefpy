from abc import ABC
from typing import Dict
from typing import List

from bs4 import BeautifulSoup
from requests import Response


class Sport(ABC):
    def __init__(self, fmt: str = "dict"):
        self._num_teams: int = 0
        self.url: str = ""
        self.response: Response = Response()
        self.soup: BeautifulSoup = BeautifulSoup()
        self.soup_attrs: Dict = {}
        self.teams: Dict = {}
        self.fmt: str = fmt

    def get_teams(self) -> dict:
        teams = dict()
        for item in self.soup.find_all(attrs=self.soup_attrs)[1 : self._num_teams + 1]:
            teams[item.find("a")["href"].split("/")[-2]] = {
                "team_name": item.text,
                "abbrev": item.find("a")["href"].split("/")[-2],
                "url": self.url + item.find("a")["href"],
            }

        return teams

    @staticmethod
    def players():
        raise NotImplementedError

    def compare_franchises(self, franchises: List[str]):
        raise NotImplementedError

    def compare_players(self, players: List[str], total="career"):
        raise NotImplementedError

    def box_score(self):
        raise NotImplementedError
