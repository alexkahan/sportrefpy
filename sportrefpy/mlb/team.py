import numpy as np
import pandas as pd

from sportrefpy.mlb.league import MLB
from sportrefpy.team.team import Team
from sportrefpy.util.enums import SportURLs


class MLBTeam(Team):
    def __init__(self, team):
        super().__init__()
        mlb = MLB()
        self._team = team.upper()
        self._details = mlb.get_teams()[self._team]

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
    def batters_url(self):
        return f"{self.team_url}bat.shtml"

    @property
    def pitchers_url(self):
        return f"{self.team_url}pitch.shtml"

    @property
    def managers_url(self):
        return f"{self.team_url}managers.shtml"

    @property
    def seasons_url(self):
        return f"{SportURLs.MLB.value}/teams/{self.abbreviation}"

    def batters_all_time_stats(self, batter=None):
        """
        Returns Pandas dataframe of all historical player data.
        """

        batters = pd.read_html(self.batters_url)[0]
        batters.drop(columns={"S", "C", "F", "Rk"}, inplace=True)
        batters = batters[batters.columns[:-1]]
        batters.dropna(axis="rows", subset="Name", inplace=True)
        batters = batters[batters["Name"] != "Name"]
        batters["Name"] = batters["Name"].apply(lambda x: x.split(" HOF")[0])
        batters.set_index("Name", inplace=True)
        batters = batters.apply(pd.to_numeric)

        if batter is not None:
            try:
                return batters.loc[batter]
            except KeyError:
                return "Player not found."

        return batters

    def pitchers_all_time_stats(self, pitcher=None):
        """
        Returns Pandas dataframe of all historical player data.
        """

        pitchers = pd.read_html(self.pitchers_url)[0]
        pitchers.drop(columns={"S", "C", "F", "Rk"}, inplace=True)
        pitchers.dropna(axis="rows", subset="Name", inplace=True)
        pitchers = pitchers[pitchers["Name"] != "Name"]
        pitchers["Name"] = pitchers["Name"].apply(lambda x: x.split(" HOF")[0])
        pitchers.set_index("Name", inplace=True)
        pitchers = pitchers.apply(pd.to_numeric)

        if pitcher is not None:
            try:
                return pitchers.loc[pitcher]
            except KeyError:
                return "Player not found."

        return pitchers

    def managers_all_time_stats(self, manager=None):
        """
        Returns Pandas dataframe of all historical coach data.
        """

        managers = pd.read_html(self.managers_url)[0]
        managers.dropna(axis="rows", subset="Mgr", inplace=True)
        managers.drop(columns={"Rk"}, inplace=True)
        managers = managers[managers["Mgr"] != "Mgr"]
        managers["Mgr"] = managers["Mgr"].apply(lambda x: x.split(" HOF")[0])
        managers.set_index("Mgr", inplace=True)
        managers = managers.apply(pd.to_numeric)

        if manager is not None:
            try:
                return managers.loc[manager]
            except KeyError:
                return "Player not found."

        return managers

    def roster(self, season=None):
        """
        Returns Pandas dataframe of roster for a given year.
        """
        roster_url = f"{self.team_url}{str(season)}-roster.shtml"
        roster = pd.read_html(roster_url, attrs={"id": "appearances"})[0]
        roster["Name"] = roster["Name"].apply(lambda x: x.split(" HOF")[0])
        roster = roster[roster["Name"] != "Name"]
        roster.set_index("Name", inplace=True)
        roster.drop(columns={"Unnamed: 2"}, inplace=True)
        roster.dropna(axis="columns", how="any", inplace=True)
        roster = roster.apply(pd.to_numeric, errors="ignore")

        return roster

    def season_history(self, year=None):
        """
        Returns Pandas dataframe of seasons.
        """

        seasons = pd.read_html(self.team_url)[0]
        seasons = seasons[seasons["Tm"] != "Tm"]
        seasons["Year"] = seasons["Year"].astype(int)
        seasons["Playoffs"] = seasons["Playoffs"].astype(str)
        seasons["Playoffs"] = seasons["Playoffs"].apply(
            lambda x: x.replace("\xa0", " ")
        )
        seasons["Playoffs"].replace("nan", np.nan, inplace=True)
        seasons.set_index("Year", inplace=True)
        seasons.drop(columns={"Tm"}, inplace=True)

        if year is not None:
            try:
                return seasons.loc[year]
            except KeyError:
                return "Season not found."

        return seasons

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise_name}>"
