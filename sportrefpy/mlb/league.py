import requests
from datetime import datetime
from bs4 import BeautifulSoup, Comment
import pandas as pd


class MLB:

    def __init__(self):
        self.url = 'https://www.baseball-reference.com'
        self.teams = {}
        if datetime.today().month >= 4:
            self.current_season_year = datetime.today().year
        else:
            self.current_season_year = datetime.today().year - 1

        response = requests.get(self.url + '/teams')
        soup = BeautifulSoup(response.text, features='lxml')

        for item in soup.find_all(attrs={'data-stat': 'franchise_name'})[1:31]:
            self.teams[item.find('a')['href'].split('/')[-2]] = {
                "team_name": item.text,
                "abbrev": item.find('a')['href'].split('/')[-2],
                "url": self.url + item.find('a')['href'],
            }

    def franchise_codes(self):
        '''
        Print list of team codes, which are used for getting a specific franchise.
        '''
        for abbrev, team_name in self.teams.items():
            print(f"{abbrev} ({team_name['team_name']})")

    def standings(self, season=None):
        '''
        Season will be current year if it's not specified. Overall standings.
        '''

        if season is None:
            season = self.current_season_year

        page = requests.get(
            f'{self.url}/leagues/majors/{str(season)}-standings.shtml')
        soup = BeautifulSoup(page.text, 'html.parser')

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        tables = []
        for comment in comments:
            if 'table' in str(comment):
                try:
                    tables.append(pd.read_html(str(comment)))
                except:
                    continue
        standings = tables[-1][0]
        standings.dropna(axis='rows', how='any', inplace=True)
        standings.rename(columns={'Tm': 'Team'}, inplace=True)
        standings.drop(columns={'Rk'}, inplace=True)
        standings.index = standings.index + 1

        return standings

    def al_standings(self, season=None):

        if season is None:
            season = self.current_season_year

        page = requests.get(
            f'{self.url}/leagues/AL/{str(season)}-standings.shtml').text
        soup = BeautifulSoup(page, 'html.parser')

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        tables = []
        for comment in comments:
            if 'table' in str(comment):
                try:
                    tables.append(pd.read_html(str(comment)))
                except:
                    continue
        standings = tables[4][0]
        standings.dropna(axis='rows', how='any', inplace=True)
        standings.rename(columns={'Tm': 'Team'}, inplace=True)
        standings.drop(columns={'Rk'}, inplace=True)
        standings.index = standings.index + 1

        return standings

    def nl_standings(self, season=None):

        if season is None:
            season = self.current_season_year

        page = requests.get(
            f'{self.url}/leagues/NL/{str(season)}-standings.shtml').text
        soup = BeautifulSoup(page, 'html.parser')

        comments = soup.find_all(string=lambda text: isinstance(text, Comment))

        tables = []
        for comment in comments:
            if 'table' in str(comment):
                try:
                    tables.append(pd.read_html(str(comment)))
                except:
                    continue
        standings = tables[4][0]
        standings.dropna(axis='rows', how='any', inplace=True)
        standings.rename(columns={'Tm': 'Team'}, inplace=True)
        standings.drop(columns={'Rk'}, inplace=True)
        standings.index = standings.index + 1

        return standings
