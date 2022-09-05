import requests
from bs4 import BeautifulSoup

from sportrefpy.player.util.all_players import AllPlayers
from sportrefpy.sport.sport import Sport
from sportrefpy.util.enums import NumTeams
from sportrefpy.util.enums import SportEnum
from sportrefpy.util.enums import SportURLs


class CBB(Sport):
    def __init__(self):
        super().__init__()
        self._name = SportEnum.CBB.value
        self._num_teams = NumTeams.CBB
        self.url = SportURLs.CBB.value
        self.response = requests.get(f"{self.url}/schools")
        self.soup = BeautifulSoup(self.response.text, features="lxml")
        self.soup_attrs = {"data-stat": "school_name"}
        self.teams = self.get_teams()

    def players(self):
        return AllPlayers.cbb_players()

    def get_teams(self):
        teams = dict()
        for item in self.soup.find_all(attrs={"data-stat": "school_name"})[
            1 : self._num_teams + 1
        ]:
            if item.find("a") is not None:
                teams[item.find("a")["href"].split("/")[-2]] = {
                    "team_name": item.text,
                    "url": "https://www.sports-reference.com" + item.find("a")["href"],
                }

        return teams

    def school_codes(self):
        """
        Print list of team codes, which are used for getting a specific schools.
        """
        for abbrev, team_name in self.schools.items():
            print(f"{abbrev} ({team_name['team_name']})")
