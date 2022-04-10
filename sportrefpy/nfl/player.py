import requests
import os

from bs4 import BeautifulSoup, Comment
import pandas as pd
import numpy as np
import enchant

from sportrefpy.nfl.league import NFL
from sportrefpy.errors.not_found import PlayerNotFound


class NFLPlayer(NFL):
    def __init__(self, player):
        super().__init__()

        player_dict = enchant.PyPWL(os.path.dirname
                                    (os.path.dirname(__file__)) + '\\assets\\nfl_players.txt')
        first_letter_last_name = player.split()[1][0].upper()
        response = requests.get(
            self.url + f'/players/{first_letter_last_name}')
        soup = BeautifulSoup(response.text, features='lxml')
        players = soup.find('div', attrs={'id': 'div_players'})
        if player in players.text:
            for choice in players:
                if player in choice.text:
                    self.full_name = player
                    self.player_url = self.url + choice.find('a')['href']
                    # response = requests.get(self.player_url)
                    # soup = BeautifulSoup(response.text, features='lxml')
                    # self.pitcher = True if 'Pitcher' in \
                    #     soup.find_all('p')[0].text else False
                    # comments = soup.find_all(string=lambda text:isinstance(text, Comment))
                    # tables = []
                    # for comment in comments:
                    #     if 'batting_postseason' in str(comment) or 'pitching_postseason' in str(comment):
                    #         tables.append(str(comment))
                    # if tables:
                    #     self.playoffs = True
                    # else:
                    #     self.playoffs = False

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

    # def regular_season_batting(self, season=None, stat=None):
    #     '''
    #     Returns a players regular seasons batting stats by career.
    #     '''
    #     if not self.pitcher:
    #         batting = pd.read_html(self.player_url, attrs={'id': 'batting_standard'})[0]
    #         batting.dropna(how='any', axis='rows', subset='Year', inplace=True)
    #         batting = batting[~batting['Year'].str.contains('Yrs|yrs|yr|Avg')]
    #         batting = batting[batting['Lg'].str.contains('NL|AL|MLB')]
    #         batting = batting.apply(pd.to_numeric, errors='ignore')
    #         batting.set_index('Year', inplace=True)
    #     elif self.pitcher:
    #         response = requests.get(self.player_url)
    #         soup = BeautifulSoup(response.text, features='lxml')
    #         comments = soup.find_all(string=lambda text:isinstance(text, Comment))
    #         tables = []
    #         for comment in comments:
    #             if 'batting_standard' in str(comment):
    #                 try:
    #                     tables.append(pd.read_html(str(comment)))
    #                 except:
    #                     continue
    #         batting = tables[0][0]
    #         batting.dropna(how='any', axis='rows', subset='Year', inplace=True)
    #         batting = batting[~batting['Year'].str.contains('Yrs|yrs|yr|Avg')]
    #         batting = batting[batting['Lg'].str.contains('NL|AL|MLB')]
    #         batting = batting.apply(pd.to_numeric, errors='ignore')
    #         batting.set_index('Year', inplace=True)

    #     if season:
    #         try:
    #             return batting.loc[season]
    #         except KeyError:
    #             return None
    #     return batting

    # def regular_season_pitching(self, season=None):
    #     '''
    #     Returns a players regular seasons pitching stats by career.
    #     '''
    #     if self.pitcher:
    #         pitching = pd.read_html(self.player_url, attrs={'id': 'pitching_standard'})[0]
    #         pitching.dropna(how='any', axis='rows', subset='Year', inplace=True)
    #         pitching = pitching[~pitching['Year'].str.contains('Yrs|yrs|yr|Avg')]
    #         pitching = pitching[pitching['Lg'].str.contains('NL|AL|MLB')]
    #         pitching = pitching.apply(pd.to_numeric, errors='ignore')
    #         pitching.set_index('Year', inplace=True)
    #         if season:
    #             try:
    #                 return pitching.loc[season]
    #             except KeyError:
    #                 return None
    #         return pitching
    #     else:
    #         return None

    # def regular_season_fielding(self, season=None):
    #     '''
    #     Returns a players regular seasons fielding stats by career.
    #     '''
    #     response = requests.get(self.player_url)
    #     soup = BeautifulSoup(response.text, features='lxml')
    #     comments = soup.find_all(string=lambda text:isinstance(text, Comment))
    #     tables = []
    #     for comment in comments:
    #         if 'standard_fielding' in str(comment):
    #             try:
    #                 tables.append(pd.read_html(str(comment)))
    #             except:
    #                 continue
    #     fielding = tables[0][0]
    #     fielding.dropna(how='any', axis='rows', subset='Year', inplace=True)
    #     fielding = fielding[~fielding['Year'].str.contains('Seasons')]
    #     fielding = fielding[fielding['Lg'].str.contains('NL|AL|MLB')]
    #     fielding = fielding.apply(pd.to_numeric, errors='ignore')
    #     fielding.set_index('Year', inplace=True)
    #     if season:
    #         try:
    #             return fielding.loc[season]
    #         except KeyError:
    #             return None
    #     return fielding

    # def post_season_batting(self, season=None):
    #     if not self.playoffs:
    #         return None
    #     response = requests.get(self.player_url)
    #     soup = BeautifulSoup(response.text, features='lxml')
    #     comments = soup.find_all(string=lambda text:isinstance(text, Comment))
    #     tables = []
    #     for comment in comments:
    #         if 'batting_postseason' in str(comment):
    #             try:
    #                 tables.append(pd.read_html(str(comment)))
    #             except:
    #                 continue
    #     batting = tables[0][0]
    #     batting.dropna(how='any', axis='rows', subset='Year', inplace=True)
    #     batting = batting[~batting['Year'].str.\
    #         contains('ALWC|NLWC|ALDS|NLDS|ALCS|NLCS|WS')]
    #     batting = batting[batting['Lg'].str.contains('NL|AL|MLB')]
    #     batting = batting.apply(pd.to_numeric, errors='ignore')
    #     batting.set_index('Year', inplace=True)
    #     if season:
    #         try:
    #             return batting.loc[season]
    #         except KeyError:
    #             return None
    #     return batting

    # def post_season_pitching(self, season=None):
    #     if not self.pitcher:
    #         return None
    #     response = requests.get(self.player_url)
    #     soup = BeautifulSoup(response.text, features='lxml')
    #     comments = soup.find_all(string=lambda text:isinstance(text, Comment))
    #     tables = []
    #     for comment in comments:
    #         if 'pitching_postseason' in str(comment):
    #             try:
    #                 tables.append(pd.read_html(str(comment)))
    #             except:
    #                 continue
    #     pitching = tables[0][0]
    #     pitching.dropna(how='any', axis='rows', subset='Year', inplace=True)
    #     pitching = pitching[~pitching['Year'].str.\
    #         contains('ALWC|NLWC|ALDS|NLDS|ALCS|NLCS|WS')]
    #     pitching = pitching[pitching['Lg'].str.contains('NL|AL|MLB')]
    #     pitching = pitching.apply(pd.to_numeric, errors='ignore')
    #     pitching.set_index('Year', inplace=True)
    #     if season:
    #         try:
    #             return pitching.loc[season]
    #         except KeyError:
    #             return None
    #     return pitching

    # def career_totals_pitching(self, stat=None):
    #     if self.pitcher:
    #         reg = pd.read_html(self.player_url, attrs={'id': 'pitching_standard'})[0]
    #         reg = reg[reg['Year'].str.contains('Yrs', na=False)]
    #         reg = reg.apply(pd.to_numeric, errors='ignore')
    #         reg.reset_index(drop=True, inplace=True)
    #         reg.drop(columns={'Year', 'Age', 'Tm', 'Lg', 'Awards'},
    #                     inplace=True)

    #         response = requests.get(self.player_url)
    #         soup = BeautifulSoup(response.text, features='lxml')
    #         comments = soup.find_all(string=lambda text:isinstance(text, Comment))
    #         tables = []
    #         for comment in comments:
    #             if 'pitching_postseason' in str(comment):
    #                 try:
    #                     tables.append(pd.read_html(str(comment)))
    #                 except:
    #                     continue
    #         post = tables[0][0]
    #         post = post[post['Year'].str.contains('Yrs', na=False)]
    #         post = post.apply(pd.to_numeric, errors='ignore')
    #         post.drop(columns={'Year', 'Age', 'Tm', 'Lg'},
    #                     inplace=True)
    #         career = reg.merge(post, how='outer')
    #         career.drop(columns={'Series', 'Rslt', 'Opp', 'WPA', 'cWPA'}, inplace=True)
    #         career = pd.DataFrame(career.sum())
    #         career.columns = ['Totals']

    #         if stat:
    #             try:
    #                 return career.loc[stat]
    #             except KeyError:
    #                 return None
    #         return career
    #     else:
    #         return None
