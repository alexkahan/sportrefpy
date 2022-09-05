from typing import Dict

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests import Response

from sportrefpy.player.player import Player
from sportrefpy.player.util.all_players import AllPlayers
from sportrefpy.player.util.career_totals import CareerTotals
from sportrefpy.util.constants import NBA_CAREER_STATS
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.formatter import Formatter


class NBAPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.full_name: str = name
        self.sport_url = SportURLs.NBA.value

    @property
    def identifying_letter(self) -> str:
        return self.name.split()[-1][0].lower()

    @property
    def players(self) -> set:
        return AllPlayers.nba_players()

    @property
    def player_url(self):
        for item in self.soup.find_all("th", attrs={"class": "left"}):
            if self.name in item.text:
                return f"{SportURLs.NBA.value}{item.find('a')['href']}"
        return None

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

        return Formatter.convert(stats, self.fmt)

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

            return Formatter.convert(stats, self.fmt)

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

        return Formatter.convert(games, self.fmt)

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

            return Formatter.convert(playoffs, self.fmt)
        else:
            return None

    # TODO: fix this to work with Formatter.output()
    def career_totals(self) -> Dict:
        """
        Find player totals (includes regular and post season)
        """
        career_totals: Dict[str, Dict] = {}
        reg = self.regular_season_stats()
        post = self.post_season_stats()
        career_totals = CareerTotals.unpack_career_stats(
            reg, post, NBA_CAREER_STATS, career_totals
        )

        return career_totals

    def __repr__(self):
        return f"<{self.full_name}>"
