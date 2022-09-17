from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup

from sportrefpy.nba.league import NBA
from sportrefpy.team.team import Team
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.formatter import Formatter


class NBATeam(Team):
    def __init__(self, team: str):
        super().__init__()
        nba = NBA()
        self._team = team.upper()
        self._details = nba.get_teams()[self._team]

    @property
    def abbreviation(self):
        return self._details["abbrev"]

    @property
    def team(self):
        return self._details["team_name"]

    @property
    def team_url(self):
        return self._details["url"]

    @property
    def players_url(self):
        return f"{self.team_url}players.html"

    @property
    def coaches_url(self):
        return f"{self.team_url}coaches.html"

    @property
    def seasons_url(self):
        return f"{SportURLs.NBA.value}/teams/{self.abbreviation}"

    @classmethod
    def compare(cls, franchises):
        franchises = [cls(franchise) for franchise in franchises]
        comparison = pd.concat(
            [franchise.season_history()[["W", "L"]].sum() for franchise in franchises],
            axis=1,
        )
        comparison.columns = [franchise.team for franchise in franchises]
        comparison = comparison.transpose()
        comparison["W%"] = comparison["W"] / (comparison["W"] + comparison["L"])
        return comparison

    def players_all_time_stats(self, player=None):
        players = pd.read_html(self.players_url)[0]
        players.columns = [
            "Rank",
            "Player",
            "From",
            "To",
            "Yrs",
            "G",
            "MP",
            "FG",
            "FGA",
            "3P",
            "3PA",
            "FT",
            "FTA",
            "ORB",
            "TRB",
            "AST",
            "STL",
            "BLK",
            "TOV",
            "PF",
            "PTS",
            "FG%",
            "3P%",
            "FT%",
            "MPG",
            "PPG",
            "RBG",
            "APG",
        ]
        players.dropna(axis="rows", subset="Player", inplace=True)
        players.drop(columns={"Rank"}, inplace=True)
        players = players[players["Player"] != "Player"]
        players.set_index("Player", inplace=True)
        players = players.apply(pd.to_numeric)

        if player is not None:
            try:
                return Formatter.convert(players.loc[player], self.fmt)
            except KeyError:
                return "Player not found."

        return Formatter.convert(players, self.fmt)

    def coaches_all_time_data(self, coach=None):
        coaches = pd.read_html(self.coaches_url)[0]
        coaches.columns = [
            "Rank",
            "Coach",
            "From",
            "To",
            "Yrs",
            "G",
            "W",
            "L",
            "W/L%",
            "W > .500",
            "Playoffs",
            "Playoff G",
            "Playoff W",
            "Playoff L",
            "Playoff W/L%",
            "Conf",
            "Champ",
        ]
        coaches.dropna(axis="rows", subset="Coach", inplace=True)
        coaches.drop(columns={"Rank"}, inplace=True)
        coaches = coaches[coaches["Coach"] != "Coach"]
        coaches.set_index("Coach", inplace=True)
        coaches = coaches.apply(pd.to_numeric)

        if coach:
            try:
                return Formatter.convert(coaches.loc[coach], self.fmt)
            except KeyError:
                return "Coach not found."

        return Formatter.convert(coaches, self.fmt)

    def roster(self, season=None):
        if season:
            response = requests.get(self.team_url)
            soup = BeautifulSoup(response.text, features="lxml")
            for i in soup.find_all("th", attrs={"class": "left"}):
                if str(season) in i.find("a")["href"]:
                    roster = pd.read_html(
                        f"{SportURLs.NBA.value}{i.find('a')['href']}"
                    )[0]
                    break
            roster.drop(columns={"Unnamed: 6"}, inplace=True)
            roster["Exp"] = roster["Exp"].replace("R", 0)
            roster["Player"] = roster["Player"].apply(lambda x: x.split("(TW)")[0])
            roster.set_index("Player", inplace=True)
            roster["Exp"] = roster["Exp"].apply(lambda x: int(x))
            roster["Birth Date"] = roster["Birth Date"].apply(
                lambda x: pd.to_datetime(x, format="%B %d, %Y").strftime("%m-%d-%Y")
            )
            return Formatter.convert(roster, self.fmt)
        else:
            return None

    def season_history(self, year=None):
        seasons = pd.read_html(self.seasons_url)[0]
        seasons = seasons[seasons["Team"] != "Team"]
        seasons.set_index("Season", inplace=True)
        seasons["Team"] = seasons["Team"].apply(lambda x: x.split("*")[0])
        seasons.drop(columns={"Unnamed: 8", "Unnamed: 15"}, inplace=True)

        if year:
            try:
                return Formatter.convert(seasons.loc[year], self.fmt)
            except KeyError:
                return "Season not found."

        return Formatter.convert(seasons, self.fmt)

    def __repr__(self):
        return f"<{self.abbreviation} - {self.team}>"
