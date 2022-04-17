import requests
from bs4 import BeautifulSoup
import pandas as pd

from sportrefpy.cbb.cbb import CBB


class CBBSchool(CBB):
    def __init__(self, school):
        super().__init__()
        self.abbreviation = school.lower()
        self.school = self.schools[self.abbreviation]["team_name"]
        self.school_url = self.schools[self.abbreviation]["url"]

    def __repr__(self):
        return f"<{self.abbreviation} - {self.school}>"

    def school_summary(self):
        response = requests.get(self.school_url)
        soup = BeautifulSoup(response.text, features="lxml")
        summary = soup.find_all("p")
        stats = [
            [item.strip() for item in stat.text.strip().replace(":", ",").split(",")]
            for stat in summary
            if stat.find("strong")
        ]
        stats = stats[:8]

        return stats

    def season_history(self):
        seasons = pd.read_html(
            self.school_url, header=[1], attrs={"id": f"{self.abbreviation}"}
        )[0]
        seasons["W"] = seasons["W"].str.replace("*", "", regex=False)
        seasons["L"] = seasons["L"].str.replace("*", "", regex=False)
        seasons["NCAA Tournament"] = seasons["NCAA Tournament"].str.replace(
            "*", "", regex=False
        )
        seasons.rename(
            columns={
                "W.1": "ConfW",
                "L.1": "ConfL",
                "W-L%.1": "ConfW-L%",
                "PTS.1": "OppPts",
            },
            inplace=True,
        )
        seasons = seasons[seasons["Rk"] != "Rk"]
        seasons.drop(columns={"Rk"}, inplace=True)
        seasons.set_index("Season", inplace=True)
        seasons = seasons.apply(pd.to_numeric, errors="ignore")

        return seasons
