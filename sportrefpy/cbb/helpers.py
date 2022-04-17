import os

from bs4 import BeautifulSoup
import requests

from sportrefpy.cbb.cbb import CBB
from sportrefpy.cbb.school import CBBSchool


def all_players():
    players = set()
    cbb = CBB()
    response = requests.get(f'{cbb.url}/players/')
    soup = BeautifulSoup(response.text, features='lxml')
    items = soup.find_all('li')
    letters = [item.find('a')['href'] for item in items if '-index.html' in item.find('a')['href']]
    print(letters)
    # with open(os.path.dirname(os.path.dirname(__file__)) + '\\assets\\cbb_players.txt', 'w', encoding='ascii') as file:
    #     for player in players:
    #         try:
    #             file.write(f'{player}\n')
    #         ex vcept UnicodeEncodeError:
    #             continue
