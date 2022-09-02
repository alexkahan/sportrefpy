from abc import ABC
from abc import abstractmethod

from sportrefpy.nba.league import NBA
from sportrefpy.sport.sport import Sport


class Team(ABC):
    @property
    def abbreviation(self):
        raise NotImplementedError

    @property
    def team(self):
        raise NotImplementedError

    @property
    def team_url(self):
        raise NotImplementedError
