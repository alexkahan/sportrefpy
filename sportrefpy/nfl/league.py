import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


class NFL:
    def __init__(self):
        self.url = "https://www.pro-football-reference.com"
        self.teams = {}
        if datetime.today().month >= 9:
            self.current_season_year = datetime.today().year
        else:
            self.current_season_year = datetime.today().year - 1

        response = requests.get(self.url + "/teams")
        soup = BeautifulSoup(response.text, features="lxml")

        for item in soup.find_all(attrs={"data-stat": "team_name", "class": "left"})[
            1:33
        ]:
            self.teams[item.find("a")["href"].split("/")[-2]] = {
                "team_name": item.text,
                "abbrev": item.find("a")["href"].split("/")[-2],
                "url": self.url + item.find("a")["href"],
            }

    def franchise_codes(self):
        """
        Print list of team codes, which are used for getting a specific franchise.
        """
        for abbrev, team_name in self.teams.items():
            print(f"{abbrev} ({team_name['team_name']})")

    def conference_standings(self, conf=None, season=None):
        """
        Season will be current year if it's not specified.
        """
        if season is None:
            season = self.current_season_year

        # AFC
        afc = pd.read_html(f"{self.url}/years/{season}", attrs={"id": "AFC"})[0]
        afc.rename(columns={"Tm": "Team"}, inplace=True)
        afc["Team"] = afc["Team"].apply(lambda x: x.split("*")[0].strip())
        afc["Team"] = afc["Team"].apply(lambda x: x.split("+")[0].strip())
        afc = afc[~afc["W"].str.contains("AFC")]
        afc = afc.apply(pd.to_numeric, errors="ignore")
        afc.drop(columns={"SRS", "OSRS", "DSRS"}, inplace=True)
        afc.sort_values(["W", "SoS", "PF"], inplace=True, ascending=False)
        afc.reset_index(inplace=True, drop=True)
        afc.index = afc.index + 1

        # NFC
        nfc = pd.read_html(f"{self.url}/years/{season}", attrs={"id": "NFC"})[0]
        nfc.rename(columns={"Tm": "Team"}, inplace=True)
        nfc["Team"] = nfc["Team"].apply(lambda x: x.split("*")[0].strip())
        nfc["Team"] = nfc["Team"].apply(lambda x: x.split("+")[0].strip())
        nfc = nfc[~nfc["W"].str.contains("NFC")]
        nfc = nfc.apply(pd.to_numeric, errors="ignore")
        nfc.drop(columns={"SRS", "OSRS", "DSRS"}, inplace=True)
        nfc.sort_values(["W", "SoS", "PF"], inplace=True, ascending=False)
        nfc.reset_index(inplace=True, drop=True)
        nfc.index = nfc.index + 1

        if conf == "AFC":
            return afc
        elif conf == "NFC":
            return nfc
        return afc, nfc

    def season_leaders(self, year=None):
        if year is None:
            season_leaders = {
                year: [None] for year in range(1966, datetime.today().year)
            }
            stats_leaders = []
            for year in range(1966, datetime.today().year):
                response = requests.get(f"{self.url}/years/{year}/")
                soup = BeautifulSoup(response.text, features="lxml")
                season_summary = soup.find_all("p")
                stats = [
                    stat.text.strip().replace(": ", ", ").split(", ")
                    for stat in season_summary
                    if stat.find("strong")
                ]
                stats = dict(
                    [stat[:2] for stat in stats if stat[0] != "Site Last Updated"]
                )
                if "League Champion" in stats.keys():
                    stats["Super Bowl Champion"] = stats.pop("League Champion")
                stats["Year"] = year
                stats_leaders.append(stats)
        season_leaders = pd.DataFrame(stats_leaders)
        season_leaders.set_index("Year", inplace=True)

        return season_leaders
