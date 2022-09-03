from typing import List

import pandas as pd

from sportrefpy.nhl.league import NHL
from sportrefpy.team.team import Team


class NHLTeam(Team):
    def __init__(self, team):
        super().__init__()
        nhl = NHL()
        self._team = team.upper()
        self._details = nhl.get_teams()[self._team]

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
    def skaters_url(self):
        return self.team_url.replace("history", "skaters")

    @property
    def goalies_url(self):
        return self.team_url.replace("history", "goalies")

    @property
    def coaches_url(self):
        return self.team_url.replace("history", "coaches")

    def skaters_all_time_stats(self, player=None):
        """
        Returns Pandas dataframe of all historical player data.
        """

        players = pd.read_html(self.skaters_url)[0]
        players.columns = [
            "Rank",
            "Player",
            "From",
            "To",
            "Yrs",
            "GP",
            "G",
            "A",
            "PTS",
            "+/-",
            "PIM",
            "EVG",
            "PPG",
            "SHG",
            "GWG",
            "EVA",
            "PPA",
            "SHA",
            "S",
            "S%",
            "TOI",
            "ATOI",
        ]
        players.dropna(axis="rows", subset="Player", inplace=True)
        players.drop(columns={"Rank", "ATOI"}, inplace=True)
        players = players[players["Player"] != "Player"]
        players["Player"] = players["Player"].str.replace("*", "", regex=False)
        players.set_index("Player", inplace=True)
        players = players.apply(pd.to_numeric)

        if player is not None:
            try:
                return players.loc[player]
            except KeyError:
                return "Player not found."

        return players

    def goalies_all_time_stats(self, goalie=None):
        """
        Returns Pandas dataframe of all historical player data.
        """

        goalies = pd.read_html(self.goalies_url)[0]
        goalies.columns = [
            "Rank",
            "Player",
            "From",
            "To",
            "Yrs",
            "GP",
            "GS",
            "W",
            "L",
            "T/O",
            "GA",
            "SA",
            "SV",
            "SV%",
            "GAA",
            "SO",
            "MIN",
            "QS",
            "QS%",
            "RBS",
            "GA%-",
            "GSAA",
            "G",
            "A",
            "PTS",
            "PIM",
        ]
        goalies.dropna(axis="rows", subset="Player", inplace=True)
        goalies.drop(columns={"Rank"}, inplace=True)
        goalies = goalies[goalies["Player"] != "Player"]
        goalies["Player"] = goalies["Player"].str.replace("*", "", regex=False)
        goalies.set_index("Player", inplace=True)
        goalies = goalies.apply(pd.to_numeric)

        if goalie is not None:
            try:
                return goalies.loc[goalie]
            except KeyError:
                return "Player not found."

        return goalies

    def coaches_all_time_data(self, coach=None):
        """
        Returns Pandas dataframe of all historical coach data.
        """

        coaches = pd.read_html(self.coaches_url, header=[1])[0]
        coaches.columns = [
            "Rank",
            "Coach",
            "From",
            "To",
            "Yrs",
            "G",
            "W",
            "L",
            "T",
            "OL",
            "PTS",
            "PTS%",
            "Playoff G",
            "Playoff W",
            "Playoff L",
            "Playoff T",
            "Playoff W-L%",
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
            roster = pd.read_html(
                io=(self.team_url.replace("history", str(season))),
                attrs={"id": "roster"},
            )[0]
            roster["Player"] = roster["Player"].apply(
                lambda x: x.split("(C)")[0].strip()
            )
            if "Salary" in roster.columns:
                roster.drop(columns={"Salary", "Draft"}, inplace=True)
            roster.set_index("Player", inplace=True)
            roster["Exp"] = roster["Exp"].replace("R", 0)
            roster["Exp"] = pd.to_numeric(roster["Exp"])
            roster.rename(
                columns={"Pos": "Position", "Ht": "Height", "Wt": "Weight"},
                inplace=True,
            )
            roster.drop(columns={"Flag", "S/C", "Summary"}, inplace=True)
            return roster
        else:
            return None

    def season_history(self, year=None):
        """
        Returns Pandas dataframe of seasons.
        """

        seasons = pd.read_html(self.team_url)[0]
        seasons = seasons[seasons["Team"] != "Team"]
        seasons.set_index("Season", inplace=True)
        seasons.drop(columns={"Lg", "Team"}, inplace=True)

        if year is not None:
            try:
                return seasons.loc[year]
            except KeyError:
                return "Season not found."

        return seasons

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"
