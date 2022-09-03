from typing import List

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from numpy.typing import DTypeLike
from requests import Response

from sportrefpy.nba.league import NBA
from sportrefpy.player.player import Player
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.player_dictionary import PlayerDictionary


class NBAPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        if not self.is_valid_player:
            PlayerDictionary.make_suggestion(NBA().player_dict, name)
        self.full_name: str = name

    @property
    def identifying_letter(self) -> str:
        return self.name.split()[-1][0].lower()

    @property
    def players(self) -> DTypeLike:
        players = pd.read_html(
            SportURLs.NBA.value + f"/players/{self.identifying_letter}"
        )[0]
        players["Player"] = players["Player"].apply(lambda x: x.split("*")[0])
        return players["Player"].values

    @property
    def player_url(self):
        for item in self.soup.find_all("th", attrs={"class": "left"}):
            if self.name in item.text:
                return f"{SportURLs.NBA.value}{item.find('a')['href']}"
        return None

    @property
    def response(self) -> Response:
        return requests.get(f"{SportURLs.NBA.value}/players/{self.identifying_letter}")

    @property
    def player_response(self) -> Response:
        return requests.get(self.player_url)

    @property
    def player_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.player_response.text, features="lxml")

    @property
    def game_log_url(self):
        return self.player_url.replace(".html", "/gamelog/")

    @property
    def playoffs(self) -> bool:
        if self.player_soup.find_all(
            "div", attrs={"id": "switcher_per_game-playoffs_per_game"}
        ):
            return True
        return False

    @property
    def playoff_url(self):
        if self.playoffs:
            return self.game_log_url.replace("gamelog", "gamelog-playoffs")
        return None

    @property
    def is_valid_player(self) -> bool:
        return self.name in self.players

    @classmethod
    def compare(cls, players, stats=None, total="career"):
        """
        Compare regular season, post season, and career totals between two players.
        """

        players = [cls(player) for player in players]
        if not stats:
            if total == "career":
                comparison = pd.concat(
                    [player.career_totals() for player in players], axis=1
                )
                comparison.columns = [player.full_name for player in players]
            elif total == "reg":
                comparison = pd.concat(
                    [player.regular_season_stats().sum() for player in players], axis=1
                )
                comparison.columns = [player.full_name for player in players]
                comparison.drop(
                    index={
                        "Age",
                        "Tm",
                        "Lg",
                        "Pos",
                        "FG%",
                        "3P%",
                        "2P%",
                        "eFG%",
                        "FT%",
                    },
                    inplace=True,
                )
            elif total == "post":
                comparison = pd.concat(
                    [player.post_season_stats().sum() for player in players], axis=1
                )
                comparison.columns = [player.full_name for player in players]
                comparison.drop(
                    index={
                        "Age",
                        "Tm",
                        "Lg",
                        "Pos",
                        "FG%",
                        "3P%",
                        "2P%",
                        "eFG%",
                        "FT%",
                    },
                    inplace=True,
                )
            return comparison
        elif stats:
            if total == "career":
                comparison = pd.concat(
                    [player.career_totals().loc[stats] for player in players], axis=1
                )
                comparison.columns = [player.full_name for player in players]
            elif total == "reg":
                comparison = pd.concat(
                    [player.regular_season_stats().sum() for player in players], axis=1
                )
                comparison.columns = [player.full_name for player in players]
                comparison.drop(
                    index={
                        "Age",
                        "Tm",
                        "Lg",
                        "Pos",
                        "FG%",
                        "3P%",
                        "2P%",
                        "eFG%",
                        "FT%",
                    },
                    inplace=True,
                )
                comparison = comparison.loc[stats]
            elif total == "post":
                comparison = pd.concat(
                    [player.post_season_stats().sum() for player in players], axis=1
                )
                comparison.columns = [player.full_name for player in players]
                comparison.drop(
                    index={
                        "Age",
                        "Tm",
                        "Lg",
                        "Pos",
                        "FG%",
                        "3P%",
                        "2P%",
                        "eFG%",
                        "FT%",
                    },
                    inplace=True,
                )
                comparison = comparison.loc[stats]
            comparison = comparison.transpose()
            comparison.columns = [stats]
            return comparison
        else:
            raise Exception

    def regular_season_stats(self) -> pd.DataFrame:
        """
        Returns a players regular seasons stats by season or by career.

        It can show stats per year in total or by team,
        if they played for multiple.
        """

        if self.playoffs:
            stats = pd.read_html(self.player_url)[2]
            stats.drop(columns={"Unnamed: 30"}, inplace=True)
        else:
            stats = pd.read_html(self.player_url)[1]
        stats.dropna(how="all", axis="rows", inplace=True)
        stats = stats[~stats["Season"].str.contains("season|Career")]
        stats.set_index("Season", inplace=True)

        return stats

    def post_season_stats(self) -> pd.DataFrame:
        """
        Returns a players postseason seasons stats (if applicable)
        by season or by career.

        It can show stats per year in total or by team,
        if they played for multiple.
        """

        if self.playoffs is False:
            return None
        else:
            stats = pd.read_html(self.player_url)[3]
            if "Unnamed: 30" in stats.columns:
                stats.drop(columns={"Unnamed: 30"}, inplace=True)
            stats.dropna(how="all", axis="rows", inplace=True)
            stats = stats[~stats["Season"].str.contains("season|Career")]
            stats.set_index("Season", inplace=True)

            return stats

    def reg_season_game_log(self, season) -> pd.Series:
        year = str(1 + int(season.split("-")[0]))
        games = pd.read_html(self.game_log_url + year)[-1]
        games.drop(columns=(["G", "Unnamed: 5"]), inplace=True)
        games.rename(
            columns={"Unnamed: 7": "Result", "Rk": "G", "GS": "Start"}, inplace=True
        )
        games = games[games["Date"] != "Date"]
        games.replace("Did Not Dress", np.nan, inplace=True)
        for column in games.columns:
            try:
                games[column] = games[column].apply(pd.to_numeric)
            except:
                continue
        games.set_index("G", inplace=True)

        return games

    def post_season_game_log(self) -> pd.Series:
        if self.playoffs:
            playoffs = pd.read_html(self.playoff_url)[-1]
            playoffs.drop(columns=(["G", "Unnamed: 5"]), inplace=True)
            playoffs.dropna(axis="rows", how="all", inplace=True)
            playoffs.rename(
                columns={"Unnamed: 8": "Result", "Rk": "G", "GS": "Start"}, inplace=True
            )
            playoffs.rename(columns={playoffs.columns[1]: "Date"}, inplace=True)
            playoffs = playoffs[playoffs["G"] != "Rk"]
            playoffs.replace("Inactive", np.nan, inplace=True)
            playoffs.reset_index(inplace=True, drop=True)
            for column in playoffs.columns:
                try:
                    playoffs[column] = pd.to_numeric(playoffs[column], errors="ignore")
                except:
                    continue
            playoffs.set_index("G", inplace=True)

            return playoffs
        else:
            return None

    def career_totals(self, stat=None) -> pd.Series:
        """
        Find player totals (includes regular and post season)
        """

        reg = self.regular_season_stats()
        reg.reset_index(inplace=True)
        post = self.post_season_stats()
        post.reset_index(inplace=True)
        career = reg.merge(post, how="outer")
        career = career[
            [
                "G",
                "GS",
                "MP",
                "FG",
                "FGA",
                "3P",
                "3PA",
                "2P",
                "2PA",
                "FT",
                "FTA",
                "ORB",
                "DRB",
                "TRB",
                "AST",
                "STL",
                "BLK",
                "TOV",
                "PF",
                "PTS",
                "Trp Dbl",
            ]
        ]
        career = pd.DataFrame(career.sum())
        career.rename(columns={0: self.full_name}, inplace=True)
        if stat:
            career = career.loc[stat]
        return career

    def __repr__(self):
        return f"<{self.full_name}>"
