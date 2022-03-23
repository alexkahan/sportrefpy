import requests
from bs4 import BeautifulSoup

class NFL:   

    def __init__(self):
        self.url = 'https://www.pro-football-reference.com'
        self.teams = {}

        response = requests.get(self.url + '/teams')
        soup = BeautifulSoup(response.text, features='lxml')

        for item in soup.find_all(attrs={'data-stat': 'team_name', 'class':'left'})[1:33]:
            self.teams[item.find('a')['href'].split('/')[-2]] = {
                "team_name": item.text,
                "url": self.url + item.find('a')['href'],
            } 

    def franchise_codes(self):
        '''
        Print list of team codes, which are used for getting a specific franchise.
        '''
        for abbrev, team_name in self.teams.items():
            print(f"{abbrev} ({team_name['team_name']})")


class NFLFranchise(NFL):
    def __init__(self, franchise):
        super().__init__()
        self.abbreviation = franchise.upper()
        self.franchise = self.teams[franchise]['team_name']
        self.url = self.teams[franchise]['url']

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"