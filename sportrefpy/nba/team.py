import pandas as pd
import requests
from bs4 import BeautifulSoup

from sportrefpy.nba.league import NBA
from sportrefpy.team.team import Team
from sportrefpy.util.enums import SportURLs


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

    def players_all_time_stats(self, player=None):
        """
        Returns Pandas dataframe of all historical player data for that team.
        """

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
                return players.loc[player]
            except KeyError:
                return "Player not found."

        return players

    def coaches_all_time_data(self, coach=None):
        """
        Returns Pandas dataframe of all historical coach data.
        """

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

        if coach is not None:
            try:
                return coaches.loc[coach]
            except KeyError:
                return "Coach not found."

        return coaches

    def roster(self, season=None):
        """
        Returns Pandas dataframe of roster for a given year.
        """
        if season:
            response = requests.get(self.team_url)
            soup = BeautifulSoup(response.text, features="lxml")
            for i in soup.find_all("th", attrs={"class": "left"}):
                if str(season) in i.find("a")["href"]:
                    roster = pd.read_html(self.url + i.find("a")["href"])[0]
                    break
            roster.drop(columns={"Unnamed: 6"}, inplace=True)
            roster["Exp"] = roster["Exp"].replace("R", 0)
            roster["Player"] = roster["Player"].apply(lambda x: x.split("(TW)")[0])
            roster.set_index("Player", inplace=True)
            roster["Exp"] = roster["Exp"].apply(lambda x: int(x))
            roster["Birth Date"] = roster["Birth Date"].apply(
                lambda x: pd.to_datetime(x)
            )
            return roster
        else:
            return None

    def season_history(self, year=None):
        """
        Returns Pandas dataframe of seasons.
        """

        seasons = pd.read_html(self.seasons_url)[0]
        seasons = seasons[seasons["Team"] != "Team"]
        seasons.set_index("Season", inplace=True)
        seasons["Team"] = seasons["Team"].apply(lambda x: x.split("*")[0])
        seasons.drop(columns={"Unnamed: 8", "Unnamed: 15"}, inplace=True)

        if year is not None:
            try:
                return seasons.loc[year]
            except KeyError:
                return "Season not found."

        return seasons

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise_name}>"
