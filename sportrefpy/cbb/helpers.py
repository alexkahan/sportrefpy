import os

from bs4 import BeautifulSoup
import requests

from sportrefpy.cbb.cbb import CBB
from sportrefpy.cbb.school import CBBSchool


def all_players():
    players = set()
    cbb = CBB()
    response = requests.get(f"{cbb.url}/players/")
    soup = BeautifulSoup(response.text, features="lxml")
    items = soup.find_all("li")
    letters = [
        item.find("a")["href"]
        for item in items
        if "-index.html" in item.find("a")["href"]
    ]
    with open(os.path.dirname(os.path.dirname(__file__)) + '\\assets\\cbb_players.txt', 'a', encoding='ascii') as file:
        for i in letters:
            response = requests.get(f'https://www.sports-reference.com{i}')
            soup = BeautifulSoup(response.text, features="lxml")
            items = soup.find_all('p')
            for item in items:
                if '(' in item.text and ')' in item.text:
                    try:
                        player = item.text.split('(')[0]
                        file.write(f'{player}\n')
                    except UnicodeEncodeError:
                        continue
