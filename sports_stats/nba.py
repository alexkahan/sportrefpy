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
                "url": self.url + item.find('a')['href'],
            }

    def franchise_codes(self):
        '''
        Print list of team codes, which are used for getting a specific franchise.
        '''
        for abbrev, team_name in self.teams.items():
            print(f"{abbrev} ({team_name['team_name']})")


class NBAFranchise(NBA):
    def __init__(self, franchise):
        super().__init__()
        self.abbreviation = franchise
        self.franchise = self.teams[franchise]['team_name']
        self.team_url = self.teams[franchise]['url']
        self.players_url = self.team_url + 'players.html'

    
    def players_all_time(self):
        self.players = {}

        response = requests.get(self.players_url)
        soup = BeautifulSoup(response.text, features='lxml')

        for item in soup.find_all(attrs={'data-stat': 'player'})[1:3]:
            self.players[item.text] = {
                "url": self.url + item.find('a')['href'],
            }

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"


sixers = NBAFranchise('PHI')
sixers.players_all_time()
print(sixers.url)
print(sixers.players)
