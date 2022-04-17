import requests
import os

from bs4 import BeautifulSoup
import pandas as pd
import enchant

from sportrefpy.cbb.cbb import CBB
from sportrefpy.errors.not_found import PlayerNotFound


class CBBPlayer(CBB):
    def __init__(self, player):
        super().__init__()

        player_dict = enchant.PyPWL(
            os.path.dirname(os.path.dirname(__file__)) + "\\assets\\cbb_players.txt"
        )
        first_letter_last_name = player.split()[-1][0].lower()
        with open(
            os.path.dirname(os.path.dirname(__file__)) + "\\assets\\cbb_players.txt",
            "r",
        ) as player_dict:
            if player in player_dict.read():
                response = requests.get(
                    f"{self.url}/cbb/players/{first_letter_last_name}-index.html"
                )
                soup = BeautifulSoup(response.text, features="lxml")
                for item in soup.find_all("p"):
                    if player in item.text.split(" (")[0]:
                        self.player_url = self.url + item.find("a")["href"]
                        self.full_name = player
            else:
                try:
                    suggestion = player_dict.suggest(player)[0]
                    message = f"""<{player}> not found. 
Is it possible you meant {suggestion}?
Player names are case-sensitive."""
                except:
                    message = f"""<{player}> not found.
Player names are case-sensitive."""
                raise PlayerNotFound(message)

    def stats_totals(self, stat=None):
        """
        Returns totals of all of a players stats
        """
        if stat is None:
            stats = pd.read_html(self.player_url, attrs={"id": "players_totals"})[0]
            stats = stats[~stats["Season"].str.contains("Career")]
            stats = stats.apply(pd.to_numeric, errors="ignore")
            stats.set_index("Season", inplace=True)

        return stats
