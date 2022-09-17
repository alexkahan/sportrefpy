from abc import ABC
from abc import abstractmethod

import pandas as pd
import requests
from bs4 import BeautifulSoup

from sportrefpy.util.enums import BoxScoreURLs
from sportrefpy.util.formatter import Formatter


class BoxScore(ABC):
    @staticmethod
    @abstractmethod
    def all_games(day, month, year):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def exact_game(day, month, year, home_team):
        raise NotImplementedError


class NBABoxScore(BoxScore):
    @staticmethod
    def all_games(day, month, year):
        raise NotImplementedError

    @staticmethod
    def exact_game(day, month, year, home_team):
        game_url = f"{BoxScoreURLs.NBA.value}{year}{Formatter.date(month)}{Formatter.date(day)}0{home_team.upper()}.html"
        response = requests.get(game_url)
        soup = BeautifulSoup(response.text, features="lxml")
        line_score = soup.find_all("table")
        away_tables = pd.read_html(game_url)[:2]
        home_tables = pd.read_html(game_url)[2:]
        return


class NHLBoxScore(BoxScore):
    @staticmethod
    def all_games(day, month, year):
        raise NotImplementedError

    @staticmethod
    def exact_game(day, month, year, home_team):
        response = requests.get(
            f"{BoxScoreURLs.NHL.value}{year}{month}{day}0{home_team}"
        )
        soup = BeautifulSoup(response.text, features="lxml")
        final_score = soup.find_all("div", {"class": "score"})
        return


class NFLBoxScore(BoxScore):
    @staticmethod
    def all_games(day, month, year):
        raise NotImplementedError

    @staticmethod
    def exact_game(day, month, year, home_team):
        raise NotImplementedError


class MLBBoxScore(BoxScore):
    @staticmethod
    def all_games(day, month, year):
        raise NotImplementedError

    @staticmethod
    def exact_game(day, month, year, home_team):
        raise NotImplementedError


class CBBBoxScore(BoxScore):
    @staticmethod
    def find_games_by_day(day, month, year):
        raise NotImplementedError

    @staticmethod
    def find_exact_game(day, month, year):
        raise NotImplementedError


class CFBBoxScore(BoxScore):
    @staticmethod
    def all_games(day, month, year):
        raise NotImplementedError

    @staticmethod
    def exact_game(day, month, year, home_team):
        raise NotImplementedError
