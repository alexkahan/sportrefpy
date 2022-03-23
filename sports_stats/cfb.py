import requests
from bs4 import BeautifulSoup

class CFB:   
 
    def __init__(self):
        self.url = 'https://www.sports-reference.com/cfb'
        self.schools = {}

        response = requests.get(self.url + '/schools')
        soup = BeautifulSoup(response.text, features='lxml')

        for item in soup.find_all(attrs={'data-stat': 'school_name'})[1:322]:
            if item.find('a') is not None:
                self.schools[item.find('a')['href'].split('/')[-2]] = {
                "team_name": item.text,
                "url": self.url + item.find('a')['href'],
                } 

    def school_codes(self):
        '''
        Print list of team codes, which are used for getting a specific schools.
        '''
        for abbrev, team_name in self.schools.items():
            print(f"{abbrev} ({team_name['team_name']})")


class CFBSchool(CFB):
    def __init__(self, school):
        super().__init__()
        self.abbreviation = school
        self.school = self.schools[school]['team_name']
        self.url = self.schools[school]['url']

    def __repr__(self):
        return f"<{self.abbreviation} - {self.school}>"