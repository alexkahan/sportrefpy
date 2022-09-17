from abc import ABC
from typing import List


class Team(ABC):
    def __init__(self, fmt: str = "dict"):
        self.fmt = fmt

    @property
    def abbreviation(self):
        raise NotImplementedError

    @property
    def team(self):
        raise NotImplementedError

    @property
    def team_url(self):
        raise NotImplementedError

    @classmethod
    def compare(cls, franchises: List[str]):
        raise NotImplementedError
