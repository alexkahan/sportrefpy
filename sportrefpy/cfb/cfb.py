import requests
from bs4 import BeautifulSoup

from sportrefpy.sport.sport import Sport
from sportrefpy.util.enums import NumTeams
from sportrefpy.util.enums import SportEnum
from sportrefpy.util.enums import SportURLs


class CFB(Sport):
    def __init__(self):
        super().__init__()
        self._name = SportEnum.CFB.value
        self._num_teams = NumTeams.CFB
        self.url = SportURLs.CFB.value
        self.response = requests.get(f"{self.url}/schools")
        self.soup = BeautifulSoup(self.response.text, features="lxml")
        self.soup_attrs = {"data-stat": "school_name"}
        self.teams = self.get_teams()

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


class CFBSchool(CFB):
    def __init__(self, school):
        super().__init__()
        self.abbreviation = school
        self.school = self.teams[school]["team_name"]
        self.school_url = self.teams[school]["url"]

    def __repr__(self):
        return f"<{self.abbreviation} - {self.school}>"
