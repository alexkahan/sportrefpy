import os

import requests
from bs4 import BeautifulSoup

from sportrefpy.cbb.cbb import CBB
from sportrefpy.mlb.league import MLB
from sportrefpy.mlb.team import MLBTeam
from sportrefpy.nba.league import NBA
from sportrefpy.nba.team import NBATeam
from sportrefpy.nfl.league import NFL
from sportrefpy.nfl.team import NFLTeam
from sportrefpy.nhl.league import NHL
from sportrefpy.nhl.team import NHLTeam


class AllPlayers:
    @staticmethod
    def nhl_players():
        players = set()
        nhl = NHL()
        for team in nhl.teams.keys():
            franchise = NHLTeam(team)
            players.update(franchise.skaters_all_time_stats().index)
            players.update(franchise.goalies_all_time_stats().index)
        return players

    @staticmethod
    def nfl_players():
        players = set()
        nfl = NFL()
        for team in nfl.teams.keys():
            franchise = NFLTeam(team)
            players.update(franchise.passer_all_time_stats().index)
            players.update(franchise.rusher_all_time_stats().index)
            players.update(franchise.receiving_all_time_stats().index)
            players.update(franchise.returns_all_time_stats().index)
            players.update(franchise.kicking_all_time_stats().index)
            players.update(franchise.scoring_all_time_stats().index)
            players.update(franchise.defense_all_time_stats().index)
        with open(
            os.path.dirname(os.path.dirname(__file__)) + "\\assets\\nfl_players.txt",
            "w",
            encoding="ascii",
        ) as file:
            for player in players:
                try:
                    player = player.replace("*", "")
                    file.write(f"{player}\n")
                except UnicodeEncodeError:
                    continue

    @staticmethod
    def nba_players():
        players = set()
        nba = NBA()
        for team in nba.teams.keys():
            franchise = NBATeam(team)
            players.update(franchise.players_all_time_stats().index)
        with open(
            os.path.dirname(os.path.dirname(__file__)) + "\\assets\\nba_players.txt",
            "w",
            encoding="ascii",
        ) as file:
            for player in players:
                try:
                    file.write(f"{player}\n")
                except UnicodeEncodeError:
                    continue

    @staticmethod
    def mlb_players():
        players = set()
        mlb = MLB()
        for team in mlb.teams.keys():
            franchise = MLBTeam(team)
            players.update(franchise.pitchers_all_time_stats().index)
            players.update(franchise.batters_all_time_stats().index)
        with open(
            os.path.dirname(os.path.dirname(__file__)) + "\\assets\\mlb_players.txt",
            "w",
            encoding="ascii",
        ) as file:
            for player in players:
                try:
                    file.write(f"{player}\n")
                except UnicodeEncodeError:
                    continue

    @staticmethod
    def cbb_players():
        players = set()
        cbb = CBB()
        response = requests.get(f"{cbb.url}/players/")
        soup = BeautifulSoup(response.text, features="lxml")
        items = soup.find_all("li")
        letters = [
            item.find("a")["href"]
            for item in items
            if "-index.html" in item.find("a")["href"]
        ]
        with open(
            os.path.dirname(os.path.dirname(__file__)) + "\\assets\\cbb_players.txt",
            "a",
            encoding="ascii",
        ) as file:
            for i in letters:
                response = requests.get(f"https://www.sports-reference.com{i}")
                soup = BeautifulSoup(response.text, features="lxml")
                items = soup.find_all("p")
                for item in items:
                    if "(" in item.text and ")" in item.text:
                        try:
                            player = item.text.split("(")[0]
                            file.write(f"{player}\n")
                        except UnicodeEncodeError:
                            continue
