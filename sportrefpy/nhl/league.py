import requests
from bs4 import BeautifulSoup
import pandas as pd

class NHL:   
 
    def __init__(self):
        self.url = 'https://www.hockey-reference.com'
        self.teams = {}
        self.standings_url = self.url + '/boxscores/'

        response = requests.get(self.url + '/teams')
        soup = BeautifulSoup(response.text, features='lxml')

        for item in soup.find_all(attrs={'data-stat': 'franch_name'})[1:33]:
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

        
    def conference_standings(self, conf=None):
        # Eastern Conference
        east_conf = pd.read_html(self.standings_url)[-2]
        east_conf.rename(columns={'Unnamed: 0': 'Team'}, inplace=True)
        east_conf = east_conf[~east_conf['Team'].str.contains('Division')]
        east_conf = east_conf.apply(pd.to_numeric, errors='ignore')
        east_conf.sort_values(['PTS', 'RgPt%', 'GF'], inplace=True, ascending=False)
        east_conf.reset_index(inplace=True, drop=True)
        east_conf.index = east_conf.index + 1

        # Western Conference
        west_conf = pd.read_html(self.standings_url)[-1]
        west_conf.rename(columns={'Unnamed: 0': 'Team'}, inplace=True)
        west_conf = west_conf[~west_conf['Team'].str.contains('Division')]
        west_conf = west_conf.apply(pd.to_numeric, errors='ignore')
        west_conf.sort_values(['PTS', 'RgPt%', 'GF'], inplace=True, ascending=False)
        west_conf.reset_index(inplace=True, drop=True)
        west_conf.index = west_conf.index + 1

        if conf == 'east':
            return east_conf
        elif conf == 'west':
            return west_conf
        return east_conf, west_conf