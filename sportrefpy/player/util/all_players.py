import requests
from bs4 import BeautifulSoup
from bs4 import Tag

from sportrefpy.util.enums import SportURLs
from sportrefpy.util.formatter import Formatter


class AllPlayers:
    @staticmethod
    def nhl_players() -> set:
        players = set()
        response = requests.get(f"{SportURLs.NHL.value}/players/")
        soup = BeautifulSoup(response.text, features="lxml")
        items = soup.find("ul", {"class": "page_index"})
        letters = [
            item.find("a") for item in items if item.find("a") and type(item) is Tag
        ]
        for letter in letters:
            response = requests.get(f"{SportURLs.NHL.value}{letter.get('href')}")
            soup = BeautifulSoup(response.text, features="lxml")
            items = soup.find_all("p")
            for item in items[2:]:
                if "(" in item.text and ")" in item.text:
                    try:
                        players.add(Formatter.clean_player_name(item.text))
                    except UnicodeEncodeError:
                        continue
        return players

    @staticmethod
    def nfl_players() -> set:
        players = set()
        response = requests.get(f"{SportURLs.NFL.value}/players/")
        soup = BeautifulSoup(response.text, features="lxml")
        items = soup.find_all("li")
        letters = [
            item.find("a")["href"]
            for item in items
            if item.find("a") and type(item) is Tag
        ]
        for letter in letters:
            if "/players/" in letter:
                response = requests.get(f"{SportURLs.NFL.value}{letter}")
                soup = BeautifulSoup(response.text, features="lxml")
                items = soup.find_all("p")
                for item in items:
                    if "(" in item.text and ")" in item.text:
                        try:
                            players.add(Formatter.clean_player_name(item.text))
                        except UnicodeEncodeError:
                            continue
        return players

    @staticmethod
    def nba_players() -> set:
        players = set()
        response = requests.get(f"{SportURLs.NBA.value}/players/")
        soup = BeautifulSoup(response.text, features="lxml")
        items = soup.find("ul", {"class": "page_index"}).find_all("li")
        letters = [
            item.find("a").get("href")
            for item in items
            if item.find("a") and type(item) is Tag
        ]
        letters = [letter for letter in letters if "/players/" in letter]
        for letter in letters[:-1]:
            response = requests.get(f"{SportURLs.NBA.value}{letter}")
            soup = BeautifulSoup(response.text, features="lxml")
            items = soup.find("tbody").find_all("tr")
            for item in items:
                # if "(" in item.text and ")" in item.text:
                try:
                    players.add(Formatter.clean_player_name(item.find("a").text))
                except UnicodeEncodeError:
                    continue
        return players

    @staticmethod
    def mlb_players() -> set:
        players = set()
        response = requests.get(f"{SportURLs.MLB.value}/players/")
        soup = BeautifulSoup(response.text, features="lxml")
        items = soup.find("ul", {"class": "page_index"}).find_all("li")
        letters = [
            item.find("a").get("href")
            for item in items
            if item.find("a") and type(item) is Tag
        ]
        for letter in letters:
            response = requests.get(f"{SportURLs.MLB.value}{letter}")
            soup = BeautifulSoup(response.text, features="lxml")
            items = soup.find_all("p")
            for item in items:
                if "(" in item.text and ")" in item.text:
                    try:
                        players.add(Formatter.clean_player_name(item.text))
                    except UnicodeEncodeError:
                        continue
        return players

    @staticmethod
    def cbb_players():
        players = set()
        response = requests.get(f"{SportURLs.CBB.value}/players/")
        soup = BeautifulSoup(response.text, features="lxml")
        items = soup.find_all("li")
        letters = [
            item.find("a")["href"]
            for item in items
            if "-index.html" in item.find("a")["href"]
        ]
        for letter in letters:
            response = requests.get(f"https://www.sports-reference.com{letter}")
            soup = BeautifulSoup(response.text, features="lxml")
            items = soup.find_all("p")
            for item in items:
                if "(" in item.text and ")" in item.text:
                    try:
                        players.add(Formatter.clean_player_name(item.text))
                    except UnicodeEncodeError:
                        continue
        return players
