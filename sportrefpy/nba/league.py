import requests
from bs4 import BeautifulSoup
import pandas as pd


class NBA:
    def __init__(self):
        self.url = "https://www.basketball-reference.com"
        self.teams = {}
        self.standings_url = self.url + "/boxscores/"

        response = requests.get(self.url + "/teams")
        soup = BeautifulSoup(response.text, features="lxml")

        for item in soup.find_all(attrs={"data-stat": "franch_name"})[1:31]:
            self.teams[item.find("a")["href"].split("/")[-2]] = {
                "team_name": item.text,
                "abbrev": item.find("a")["href"].split("/")[-2],
                "url": self.url + item.find("a")["href"],
            }

    def franchise_codes(self):
        """
        Print list of team codes, which are used for getting a specific franchise.
        """
        for team in self.teams.items():
            print(f"{team[1]['abbrev']} ({team[1]['team_name']})")

    def conference_standings(self, conf=None):
        east_conf = pd.read_html(self.standings_url)[-2]
        east_conf.index = east_conf.index + 1
        east_conf.replace("—", 0, inplace=True)
        east_conf["GB"] = pd.to_numeric(east_conf["GB"])
        west_conf = pd.read_html(self.standings_url)[-1]
        west_conf.index = west_conf.index + 1
        west_conf.replace("—", 0, inplace=True)
        west_conf["GB"] = pd.to_numeric(west_conf["GB"])
        if conf == "east":
            return east_conf
        elif conf == "west":
            return west_conf
        return east_conf, west_conf
