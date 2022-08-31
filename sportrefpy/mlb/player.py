import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4 import Comment
from requests import Response

from sportrefpy.mlb.league import MLB
from sportrefpy.player.player import Player
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.player_dictionary import PlayerDictionary


class MLBPlayer(Player):
    @property
    def identifying_letter(self):
        return self.name.split()[1][0].lower()

    @property
    def players(self):
        return self.soup.find("div", attrs={"id": "div_players_"})

    @property
    def player_url(self):
        for choice in self.players:
            if self.name in choice.text:
                return f"{SportURLs.MLB.value}{choice.find('a')['href']}"

    @property
    def response(self):
        return requests.get(f"{SportURLs.MLB.value}/players/{self.identifying_letter}")

    @property
    def player_response(self) -> Response:
        return requests.get(self.player_url)

    @property
    def player_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.player_response.text, features="lxml")

    @property
    def is_pitcher(self) -> bool:
        return "Pitcher" in self.player_soup.find_all("p")[0].text

    @property
    def playoffs(self):
        comments = self.player_soup.find_all(
            string=lambda text: isinstance(text, Comment)
        )
        tables = []
        for comment in comments:
            if "batting_postseason" in str(comment) or "pitching_postseason" in str(
                comment
            ):
                tables.append(str(comment))
        if tables:
            return True
        else:
            return False

    @property
    def is_valid_player(self):
        return self.name in self.players.text

    def __init__(self, name):
        super().__init__(name)
        if not self.is_valid_player:
            PlayerDictionary.make_suggestion(MLB().player_dict, name)
        self.full_name: str = name
        # self.soup_attrs = {"id": "div_players_"}

    def regular_season_batting(self, season=None, stat=None):
        """
        Returns a players regular seasons batting stats by career.
        """
        if not self.is_pitcher:
            batting = pd.read_html(self.player_url, attrs={"id": "batting_standard"})[0]
            batting.dropna(how="any", axis="rows", subset="Year", inplace=True)
            batting = batting[~batting["Year"].str.contains("Yrs|yrs|yr|Avg")]
            batting = batting[batting["Lg"].str.contains("NL|AL|MLB")]
            batting = batting.apply(pd.to_numeric, errors="ignore")
            batting.set_index("Year", inplace=True)
        elif self.is_pitcher:
            response = requests.get(self.player_url)
            soup = BeautifulSoup(response.text, features="lxml")
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            tables = []
            for comment in comments:
                if "batting_standard" in str(comment):
                    try:
                        tables.append(pd.read_html(str(comment)))
                    except:
                        continue
            batting = tables[0][0]
            batting.dropna(how="any", axis="rows", subset="Year", inplace=True)
            batting = batting[~batting["Year"].str.contains("Yrs|yrs|yr|Avg")]
            batting = batting[batting["Lg"].str.contains("NL|AL|MLB")]
            batting = batting.apply(pd.to_numeric, errors="ignore")
            batting.set_index("Year", inplace=True)

        if season:
            try:
                return batting.loc[season]
            except KeyError:
                return None
        return batting

    def regular_season_pitching(self, season=None):
        """
        Returns a players regular seasons pitching stats by career.
        """
        if self.is_pitcher:
            pitching = pd.read_html(self.player_url, attrs={"id": "pitching_standard"})[
                0
            ]
            pitching.dropna(how="any", axis="rows", subset="Year", inplace=True)
            pitching = pitching[~pitching["Year"].str.contains("Yrs|yrs|yr|Avg")]
            pitching = pitching[pitching["Lg"].str.contains("NL|AL|MLB")]
            pitching = pitching.apply(pd.to_numeric, errors="ignore")
            pitching.set_index("Year", inplace=True)
            if season:
                try:
                    return pitching.loc[season]
                except KeyError:
                    return None
            return pitching
        else:
            return None

    def regular_season_fielding(self, season=None):
        """
        Returns a players regular seasons fielding stats by career.
        """
        response = requests.get(self.player_url)
        soup = BeautifulSoup(response.text, features="lxml")
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        tables = []
        for comment in comments:
            if "standard_fielding" in str(comment):
                try:
                    tables.append(pd.read_html(str(comment)))
                except:
                    continue
        fielding = tables[0][0]
        fielding.dropna(how="any", axis="rows", subset="Year", inplace=True)
        fielding = fielding[~fielding["Year"].str.contains("Seasons")]
        fielding = fielding[fielding["Lg"].str.contains("NL|AL|MLB")]
        fielding = fielding.apply(pd.to_numeric, errors="ignore")
        fielding.set_index("Year", inplace=True)
        if season:
            try:
                return fielding.loc[season]
            except KeyError:
                return None
        return fielding

    def post_season_batting(self, season=None):
        if not self.playoffs:
            return None
        response = requests.get(self.player_url)
        soup = BeautifulSoup(response.text, features="lxml")
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        tables = []
        for comment in comments:
            if "batting_postseason" in str(comment):
                try:
                    tables.append(pd.read_html(str(comment)))
                except:
                    continue
        batting = tables[0][0]
        batting.dropna(how="any", axis="rows", subset="Year", inplace=True)
        batting = batting[
            ~batting["Year"].str.contains("ALWC|NLWC|ALDS|NLDS|ALCS|NLCS|WS")
        ]
        batting = batting[batting["Lg"].str.contains("NL|AL|MLB")]
        batting = batting.apply(pd.to_numeric, errors="ignore")
        batting.set_index("Year", inplace=True)
        if season:
            try:
                return batting.loc[season]
            except KeyError:
                return None
        return batting

    def post_season_pitching(self, season=None):
        if not self.is_pitcher:
            return None
        response = requests.get(self.player_url)
        soup = BeautifulSoup(response.text, features="lxml")
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        tables = []
        for comment in comments:
            if "pitching_postseason" in str(comment):
                try:
                    tables.append(pd.read_html(str(comment)))
                except:
                    continue
        pitching = tables[0][0]
        pitching.dropna(how="any", axis="rows", subset="Year", inplace=True)
        pitching = pitching[
            ~pitching["Year"].str.contains("ALWC|NLWC|ALDS|NLDS|ALCS|NLCS|WS")
        ]
        pitching = pitching[pitching["Lg"].str.contains("NL|AL|MLB")]
        pitching = pitching.apply(pd.to_numeric, errors="ignore")
        pitching.set_index("Year", inplace=True)
        if season:
            try:
                return pitching.loc[season]
            except KeyError:
                return None
        return pitching

    def career_totals_pitching(self, stat=None):
        if self.is_pitcher:
            reg = pd.read_html(self.player_url, attrs={"id": "pitching_standard"})[0]
            reg = reg[reg["Year"].str.contains("Yrs", na=False)]
            reg = reg.apply(pd.to_numeric, errors="ignore")
            reg.reset_index(drop=True, inplace=True)
            reg.drop(columns={"Year", "Age", "Tm", "Lg", "Awards"}, inplace=True)

            response = requests.get(self.player_url)
            soup = BeautifulSoup(response.text, features="lxml")
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            tables = []
            for comment in comments:
                if "pitching_postseason" in str(comment):
                    try:
                        tables.append(pd.read_html(str(comment)))
                    except:
                        continue
            post = tables[0][0]
            post = post[post["Year"].str.contains("Yrs", na=False)]
            post = post.apply(pd.to_numeric, errors="ignore")
            post.drop(columns={"Year", "Age", "Tm", "Lg"}, inplace=True)
            career = reg.merge(post, how="outer")
            career.drop(columns={"Series", "Rslt", "Opp", "WPA", "cWPA"}, inplace=True)
            career = pd.DataFrame(career.sum())
            career.columns = ["Totals"]

            if stat:
                try:
                    return career.loc[stat]
                except KeyError:
                    return None
            return career
        else:
            return None
