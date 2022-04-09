import requests
import os

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import enchant

from sportrefpy.nhl.league import NHL
from sportrefpy.errors.not_found import PlayerNotFound


class NHLPlayer(NHL):
    def __init__(self, player):
        super().__init__()\

        player_dict = enchant.PyPWL(os.path.dirname
                                    (os.path.dirname(__file__)) + '\\assets\\nhl_players.txt')
        first_letter = player.split()[-1][0].lower()
        with open(os.path.dirname(os.path.dirname(__file__)) + '\\assets\\nhl_players.txt', 'r') as player_dict:
            if player in player_dict.read():
                response = requests.get(self.url + f'/players/{first_letter}')
                soup = BeautifulSoup(response.text, features='lxml')
                for item in soup.find_all('p', attrs={'class': 'nhl'}):
                    if player in item.text.split(' (')[0]:
                        self.player_url = self.url + item.find('a')['href']
                        self.full_name = player
            else:
                try:
                    suggestion = player_dict.suggest(player)[0]
                    message = f'''<{player}> not found. 
Is it possible you meant {suggestion}?
Player names are case-sensitive.'''
                except:
                    message = f'''<{player}> not found.
Player names are case-sensitive.'''
                raise PlayerNotFound(message)

    def regular_season_stats(self):
        '''
        Returns a players regular seasons stats by season or by career.

        It can show stats per year in total or by team, 
        if they played for multiple.
        '''

        stats = pd.read_html(self.player_url, header=[1])[0]
        stats.columns = ['Season', 'Age', 'Tm', 'Lg', 'GP', 'G', 'A', 'PTS',
                         '+/-', 'PIM', 'EVG', 'PPG', 'SHG', 'GWG', 'EVA', 'PPA', 'SHA',
                         'S', 'S%', 'TOI', 'ATOI', 'Awards']
        stats = stats[~stats['Season'].str.contains('season|Career|yr|yrs')]
        stats.set_index('Season', inplace=True)
        stats = stats[stats['Lg'] == 'NHL']
        stats.drop(columns={'Lg', 'TOI', 'ATOI'}, inplace=True)

        return stats
