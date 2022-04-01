import requests

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import enchant

from sports_stats.nba.league import NBA
from sports_stats.errors.not_found import PlayerNotFound


class NBAPlayer(NBA):
    def __init__(self, player):
        super().__init__()
        
        self.player_dict = enchant.PyPWL('sports_stats/assets/nba_players.txt')
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
                    self.game_log_url = self.player_url.\
                        replace('.html', '/gamelog/')
                    if soup.find_all('div', \
                        attrs={'id': 'switcher_per_game-playoffs_per_game'}):
                        self.playoffs = True
                        self.playoff_url = self.game_log_url.\
                            replace('gamelog', 'gamelog-playoffs')
                    else:
                        self.playoffs = False
                self.full_name = player
        else:
            suggestion = self.player_dict.suggest(player)[0]
            message = f'''
{player} not found. Is it possible you meant {suggestion}?
Player names are case-sensitive.'''
            raise PlayerNotFound(message)

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
        stats = stats[~stats['Season'].str.contains('season|Career')]
        stats.set_index('Season', inplace=True)

        return stats

    
    def post_season_stats(self):
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
            if 'Unnamed: 30' in stats.columns:
                stats.drop(columns={'Unnamed: 30'}, inplace=True)
            stats.dropna(how='all', axis='rows', inplace=True)
            stats = stats[~stats['Season'].str.contains('season|Career')]
            stats.set_index('Season', inplace=True)

            return stats

    
    def reg_season_game_log(self, season=None):
        if season:
            year = str(1 + int(season.split('-')[0]))
        games = pd.read_html(self.game_log_url + year)[-1]
        games.drop(columns=(['G', 'Unnamed: 5']), inplace=True)
        games.rename(columns={
            'Unnamed: 7': 'Result', 
            'Rk': 'G', 
            'GS': 'Start'}, 
            inplace=True)
        games = games[games['Date'] != 'Date']
        games.replace('Did Not Dress', np.nan, inplace=True)
        for column in games.columns:
                try:
                    games[column] = games[column].apply(pd.to_numeric)
                except:
                    continue
        games.set_index('G', inplace=True)

        return games


    def post_season_game_log(self):
            if self.playoffs:
                playoffs = pd.read_html(self.playoff_url)[-1]
                playoffs.drop(columns=(['G', 'Unnamed: 5']), inplace=True)
                playoffs.dropna(axis='rows', how='all', inplace=True)
                playoffs.rename(columns={
                    'Unnamed: 8': 'Result', 
                    'Rk': 'G', 
                    'GS': 'Start'}, 
                    inplace=True)
                playoffs.rename(columns={playoffs.columns[1]: 'Date'}, inplace=True)
                playoffs = playoffs[playoffs['G'] != 'Rk']
                playoffs.replace('Inactive', np.nan, inplace=True)
                playoffs.reset_index(inplace=True, drop=True)
                for column in playoffs.columns:
                        try:
                            playoffs[column] = pd.to_numeric(playoffs[column], errors='ignore')
                        except:
                            continue
                playoffs.set_index('G', inplace=True)

                return playoffs
            else:
                return None

    
    def career_totals(self):
        '''
        Find player totals (includes regular and post season)
        '''

        reg = self.regular_season_stats()
        reg.reset_index(inplace=True)
        post = self.post_season_stats()
        post.reset_index(inplace=True)
        career = reg.merge(post, how='outer')
        career = career[['G', 'GS', 'MP', 'FG', 'FGA', '3P', '3PA', '2P',\
             '2PA', 'FT', 'FTA', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', \
            'TOV', 'PF', 'PTS', 'Trp Dbl']]
        career = pd.DataFrame(career.sum())
        career.rename(columns={0: 'Total'}, inplace=True)
        return career


    def __repr__(self):
        return f"<{self.full_name}>"