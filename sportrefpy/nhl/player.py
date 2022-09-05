import pandas as pd

from sportrefpy.player.player import Player
from sportrefpy.player.util.all_players import AllPlayers
from sportrefpy.util.enums import SportURLs
from sportrefpy.util.formatter import Formatter


class NHLPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.full_name: str = name
        self.sport_url = SportURLs.NHL.value

    @property
    def identifying_letter(self):
        return self.name.split()[-1][0].lower()

    @property
    def players(self) -> set:
        return AllPlayers.nhl_players()

    @property
    def player_url(self):
        for item in self.soup.find_all("p", attrs={"class": "nhl"}):
            if self.name in item.text.split(" (")[0]:
                return f"{SportURLs.NHL.value}{item.find('a')['href']}"

    def regular_season_stats(self):
        """
        Returns a players regular seasons stats by season or by career.

        It can show stats per year in total or by team,
        if they played for multiple.
        """

        stats = pd.read_html(self.player_url, header=[1])[0]
        stats.columns = [
            "Season",
            "Age",
            "Tm",
            "Lg",
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
            "Awards",
        ]
        stats = stats[~stats["Season"].str.contains("season|Career|yr|yrs")]
        stats.set_index("Season", inplace=True)
        stats = stats[stats["Lg"] == "NHL"]
        stats.drop(columns={"Lg", "TOI", "ATOI"}, inplace=True)

        return Formatter.convert(stats, self.fmt)
