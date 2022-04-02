import requests
from bs4 import BeautifulSoup

class CBB:   
 
    def __init__(self):
        self.url = 'https://www.sports-reference.com/cbb'
        self.schools = {}

        response = requests.get(self.url + '/schools')
        soup = BeautifulSoup(response.text, features='lxml')

        for item in soup.find_all(attrs={'data-stat': 'school_name'})[1:510]:
            if item.find('a') is not None:
                self.schools[item.find('a')['href'].split('/')[-2]] = {
                "team_name": item.text,
                "url": 'https://www.sports-reference.com' + item.find('a')['href'],
                } 

    def school_codes(self):
        '''
        Print list of team codes, which are used for getting a specific schools.
        '''
        for abbrev, team_name in self.schools.items():
            print(f"{abbrev} ({team_name['team_name']})")


class CBBSchool(CBB):
    def __init__(self, school):
        super().__init__()
        self.abbreviation = school
        self.school = self.schools[school]['team_name']
        self.school_url = self.schools[school]['url']

    def __repr__(self):
        return f"<{self.abbreviation} - {self.school}>"