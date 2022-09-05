from abc import ABC
from abc import abstractmethod

import requests
from bs4 import BeautifulSoup

from sportrefpy.util.enums import BoxScoreURLs


class BoxScore(ABC):
    @staticmethod
    @abstractmethod
    def find_games_by_day(day, month, year):
        raise NotImplementedError

    @abstractmethod
    def find_exact_game(self, day, month, year):
        raise NotImplementedError


class NBABoxScore(BoxScore):
    @staticmethod
    def find_games_by_day(day, month, year):
        raise NotImplementedError

    def find_exact_game(self, day, month, year):
        raise NotImplementedError


class NHLBoxScore(BoxScore):
    def find_games_by_day(self, day, month, year):
        pass

    def find_exact_game(self, day, month, year):
        raise NotImplementedError


class NFLBoxScore(BoxScore):
    def find_games_by_day(self, day, month, year):
        pass

    def find_exact_game(self, day, month, year):
        raise NotImplementedError


class MLBBoxScore(BoxScore):
    def find_games_by_day(self, day, month, year):
        pass

    def find_exact_game(self, day, month, year):
        raise NotImplementedError


class CBBBoxScore(BoxScore):
    def find_games_by_day(self, day, month, year):
        pass

    def find_exact_game(self, day, month, year):
        raise NotImplementedError


class CFBBoxScore(BoxScore):
    def find_games_by_day(self, day, month, year):
        pass

    def find_exact_game(self, day, month, year):
        raise NotImplementedError
