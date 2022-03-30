import requests
from bs4 import BeautifulSoup


class NBA:   

    def __init__(self):
        self.url = 'https://www.basketball-reference.com'
        self.teams = {}

        response = requests.get(self.url + '/teams')
        soup = BeautifulSoup(response.text, features='lxml')

        for item in soup.find_all(attrs={'data-stat': 'franch_name'})[1:31]:
            self.teams[item.find('a')['href'].split('/')[-2]] = {
                "team_name": item.text,
                "abbrev": item.find('a')['href'].split('/')[-2],
                "url": self.url + item.find('a')['href'],
            }


    def franchise_codes(self):
        '''
        Print list of team codes, which are used for getting a specific franchise.
        '''
        for team in self.teams.items():
            print(f"{team[1]['abbrev']} ({team[1]['team_name']})")