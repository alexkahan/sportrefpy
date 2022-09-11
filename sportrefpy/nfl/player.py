import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests import Response

from sportrefpy.player.player import Player
from sportrefpy.player.util.all_players import AllPlayers
from sportrefpy.player.util.table_parser import TableParser
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.formatter import ColumnFormatter
from sportrefpy.util.formatter import Formatter


class NFLPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.full_name: str = name
        self.sport_url = SportURLs.NFL.value

    @property
    def identifying_letter(self):
        return self.name.split()[1][0].upper()

    @property
    def players(self) -> dict:
        return AllPlayers.nfl_players()

    @property
    def player_response(self) -> Response:
        return requests.get(self.player_url)

    @property
    def player_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.player_response.text, features="lxml")

    def regular_season_offensive_stats(self):
        table_ids = TableParser.parse_table_ids(self.player_soup, "stats_table")
        attr_id = TableParser.parse_attr_id(
            table_ids, ["receiving_and_rushing", "rushing_and_receiving"]
        )
        if not attr_id:
            return None

        df = pd.read_html(self.player_url, attrs={"id": attr_id})[0]
        df.columns = ColumnFormatter.output(df.columns.values)
        df["Year"] = df["Year"].apply(Formatter.clean_index_year)
        df = df.apply(pd.to_numeric, errors="ignore")
        df = df[~df["Year"].str.contains("season|Career|yr|yrs|nan")]
        df.set_index("Year", inplace=True)

        return Formatter.convert(df, self.fmt)

    def post_season_offensive_stats(self):
        table_ids = TableParser.parse_table_ids(self.player_soup, "stats_table")
        attr_id = TableParser.parse_attr_id(
            table_ids,
            ["receiving_and_rushing_playoffs", "rushing_and_receiving_playoffs"],
        )
        if not attr_id:
            return None

        df = pd.read_html(self.player_url, attrs={"id": attr_id})[0]
        df.columns = ColumnFormatter.output(df.columns)
        df["Year"] = df["Year"].apply(Formatter.clean_index_year)
        df = df.apply(pd.to_numeric, errors="ignore")
        df = df[~df["Year"].str.contains("season|Career|yr|yrs|nan")]
        df.set_index("Year", inplace=True)

        return Formatter.convert(df, self.fmt)

    def regular_season_passing_stats(self):
        table_ids = TableParser.parse_table_ids(self.player_soup, "stats_table")
        attr_id = TableParser.parse_attr_id(
            table_ids,
            ["passing"],
        )
        if not attr_id:
            return None

        df = pd.read_html(self.player_url, attrs={"id": attr_id})[0]
        df.columns = ColumnFormatter.output(df.columns.values)
        df["Year"] = df["Year"].apply(Formatter.clean_index_year)
        df = df.apply(pd.to_numeric, errors="ignore")
        df = df[~df["Year"].str.contains("season|Career|yr|yrs|nan")]
        df.set_index("Year", inplace=True)

        return Formatter.convert(df, self.fmt)

    def post_season_passing_stats(self):
        table_ids = TableParser.parse_table_ids(self.player_soup, "stats_table")
        attr_id = TableParser.parse_attr_id(
            table_ids,
            ["passing_playoffs"],
        )
        if not attr_id:
            return None

        df = pd.read_html(self.player_url, attrs={"id": attr_id})[0]
        df.columns = ColumnFormatter.output(df.columns.values)
        df["Year"] = df["Year"].apply(Formatter.clean_index_year)
        df = df.apply(pd.to_numeric, errors="ignore")
        df = df[~df["Year"].str.contains("season|Career|yr|yrs|nan")]
        df.set_index("Year", inplace=True)

        return Formatter.convert(df, self.fmt)

    def regular_season_return_stats(self):
        table_ids = TableParser.parse_table_ids(self.player_soup, "stats_table")
        attr_id = TableParser.parse_attr_id(
            table_ids,
            ["returns"],
        )
        if not attr_id:
            return None

        df = pd.read_html(self.player_url, attrs={"id": attr_id})[0]
        df.columns = ColumnFormatter.output(df.columns.values)
        df["Year"] = df["Year"].apply(Formatter.clean_index_year)
        df = df.apply(pd.to_numeric, errors="ignore")
        df = df[~df["Year"].str.contains("season|Career|yr|yrs|nan")]
        df.set_index("Year", inplace=True)

        return Formatter.convert(df, self.fmt)

    def post_season_return_stats(self):
        table_ids = TableParser.parse_table_ids(self.player_soup, "stats_table")
        attr_id = TableParser.parse_attr_id(
            table_ids,
            ["returns_playoffs"],
        )
        if not attr_id:
            return None

        df = pd.read_html(self.player_url, attrs={"id": attr_id})[0]
        df.columns = ColumnFormatter.output(df.columns.values)
        df["Year"] = df["Year"].apply(Formatter.clean_index_year)
        df = df.apply(pd.to_numeric, errors="ignore")
        df = df[~df["Year"].str.contains("season|Career|yr|yrs|nan")]
        df.set_index("Year", inplace=True)

        return Formatter.convert(df, self.fmt)

    def regular_season_scoring_stats(self):
        table_ids = TableParser.parse_table_ids(self.player_soup, "stats_table")
        attr_id = TableParser.parse_attr_id(
            table_ids,
            ["scoring"],
        )
        if not attr_id:
            return None

        df = pd.read_html(self.player_url, attrs={"id": attr_id})[0]
        df.columns = ColumnFormatter.output(df.columns.values)
        df["Year"] = df["Year"].apply(Formatter.clean_index_year)
        df = df.apply(pd.to_numeric, errors="ignore")
        df = df[~df["Year"].str.contains("season|Career|yr|yrs|nan")]
        df.set_index("Year", inplace=True)

        return Formatter.convert(df, self.fmt)

    def post_season_scoring_stats(self):
        table_ids = TableParser.parse_table_ids(self.player_soup, "stats_table")
        attr_id = TableParser.parse_attr_id(
            table_ids,
            ["scoring_playoffs"],
        )
        if not attr_id:
            return None

        df = pd.read_html(self.player_url, attrs={"id": attr_id})[0]
        df.columns = ColumnFormatter.output(df.columns.values)
        df["Year"] = df["Year"].apply(Formatter.clean_index_year)
        df = df.apply(pd.to_numeric, errors="ignore")
        df = df[~df["Year"].str.contains("season|Career|yr|yrs|nan")]
        df.set_index("Year", inplace=True)

        return Formatter.convert(df, self.fmt)
