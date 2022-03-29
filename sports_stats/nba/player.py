import requests
from bs4 import BeautifulSoup
from sports_stats.nba.league import NBA
import pandas as pd


class NBAPlayer(NBA):
    def __init__(self, player):
        super().__init__()
        
        first_letter = player.split()[-1][0].lower()
        players = pd.read_html(self.url + f'/players/{first_letter}')[0]
        players['Player'] = players['Player'].apply(lambda x: x.split('*')[0])
        if player in players['Player'].values:
            response = requests.get(self.url + f'/players/{first_letter}')
            soup = BeautifulSoup(response.text, features='lxml')
            for item in soup.find_all('th', attrs={'class': 'left'}):
                if player in item.text:
                    self.player_url = self.url + item.find('a')['href']
                    response = requests.get(self.player_url)
                    soup = BeautifulSoup(response.text, features='lxml')
                    if soup.find_all('div', attrs={'id': 'switcher_per_game-playoffs_per_game'}):
                        self.playoffs = True
                    else:
                        self.playoffs = False

    def regular_season_stats(self):
        '''
        Returns a players regular seasons stats by season or by career.

        It can show stats per year in total or by team, 
        if they played for multiple.
        '''
        
        if self.playoffs == True:
            stats = pd.read_html(self.player_url)[2]
            stats.drop(columns={'Unnamed: 30'}, inplace=True)
        else:
            stats = pd.read_html(self.player_url)[1]
        stats.dropna(how='all', axis='rows', inplace=True)
        stats = stats[~stats['Season'].str.contains('season')]
        stats.set_index('Season', inplace=True)

        return stats

    
    def postseason_season_stats(self):
        '''
        Returns a players postseason seasons stats (if applicable) 
        by season or by career.
        
        It can show stats per year in total or by team, 
        if they played for multiple.
        '''
        
        if self.playoffs is False:
            return None
        else:
            stats = pd.read_html(self.player_url)[3]
            # stats.drop(columns={'Unnamed: 30'}, inplace=True)
            stats.dropna(how='all', axis='rows', inplace=True)
            stats = stats[~stats['Season'].str.contains('season')]
            stats.set_index('Season', inplace=True)

            return stats
