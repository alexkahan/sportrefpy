from abc import ABC
from typing import List

from sportrefpy.util.player_checker import PlayerChecker


class Sport(ABC):
    def __init__(self):
        self._name = None
        self._num_teams = None
        self.url = None
        self.response = None
        self.soup = None
        self.soup_attrs = None
        self.teams = None

    @staticmethod
    def players():
        raise NotImplementedError

    @staticmethod
    def compare_franchises(franchises: List[str]):
        raise NotImplementedError

    def get_teams(self) -> dict:
        teams = dict()
        for item in self.soup.find_all(attrs=self.soup_attrs)[1 : self._num_teams + 1]:
            teams[item.find("a")["href"].split("/")[-2]] = {
                "team_name": item.text,
                "abbrev": item.find("a")["href"].split("/")[-2],
                "url": self.url + item.find("a")["href"],
            }

        return teams

    def franchise_codes(self) -> None:
        for abbrev, team_name in self.teams.items():
            print(f"{abbrev} ({team_name['team_name']})")
