import pandas as pd
from sports_stats.mlb.league import MLB
import numpy as np

class MLBFranchise(MLB):
    def __init__(self, franchise):
        super().__init__()
        self.abbreviation = franchise
        self.franchise = self.teams[franchise]['team_name']
        self.team_url = self.teams[franchise]['url']
        self.batters_url = self.team_url + 'bat.shtml'
        self.pitchers_url = self.team_url + 'pitch.shtml'
        self.managers_url = self.team_url + 'managers.shtml'
        self.current_roster_url = f'{self.url}/contracts/{self.abbreviation}.html'
        self.seasons_url = f'{self.url}/teams/{self.abbreviation}'

    
    def batters_all_time_stats(self):
        '''
        Returns Pandas dataframe of all historical player data.
        '''

        players = pd.read_html(self.batters_url)[0]
        players.drop(columns={'S', 'C', 'F'}, inplace=True)
        players = players[players.columns[:-1]]
        players.dropna(axis='rows', subset='Name', inplace=True)
        players = players[players['Name'] != 'Name']
        players['Name'] = players['Name'].apply(lambda x: x.split(' HOF')[0])
        players.set_index('Name', inplace=True)
        players = players.apply(pd.to_numeric)
        
        return players

    def pitchers_all_time_stats(self):
        '''
        Returns Pandas dataframe of all historical player data.
        '''

        pitchers = pd.read_html(self.pitchers_url)[0]
        pitchers.drop(columns={'S', 'C', 'F'}, inplace=True)
        pitchers.dropna(axis='rows', subset='Name', inplace=True)
        pitchers = pitchers[pitchers['Name'] != 'Name']
        pitchers['Name'] = pitchers['Name'].apply(lambda x: x.split(' HOF')[0])
        pitchers.set_index('Name', inplace=True)
        pitchers = pitchers.apply(pd.to_numeric)
        
        return pitchers

    def managers_all_time_data(self):
        '''
        Returns Pandas dataframe of all historical coach data.
        '''

        managers = pd.read_html(self.managers_url)[0]
        managers.dropna(axis='rows', subset='Mgr', inplace=True)
        managers.drop(columns={'Rk'}, inplace=True)
        managers = managers[managers['Mgr'] != 'Mgr']
        managers['Mgr'] = managers['Mgr'].apply(lambda x: x.split(' HOF')[0])
        managers.set_index('Mgr', inplace=True)
        managers = managers.apply(pd.to_numeric)

        return managers


    # def current_roster(self):
    #     '''
    #     Returns Pandas dataframe of current roster.
    #     '''

    #     current_roster = pd.read_html(self.current_roster_url)[0]
    #     current_roster = current_roster[current_roster.columns[:2]]
    #     current_roster.columns = ['Player', 'Age']
    #     current_roster = current_roster[current_roster['Player']\
    #          != 'Team Totals']
    #     current_roster.set_index('Player', inplace=True)
    #     current_roster['Age'] = current_roster['Age'].apply(lambda x: int(x))

    #     return current_roster

    
    def season_history(self):
        '''
        Returns Pandas dataframe of seasons.
        '''

        seasons = pd.read_html(self.team_url)[0]
        seasons = seasons[seasons['Tm'] != 'Tm']
        seasons['Year'] = seasons['Year'].astype(int)
        seasons['Playoffs'] = seasons['Playoffs'].astype(str)
        seasons['Playoffs'] = seasons['Playoffs']\
            .apply(lambda x: x.replace('\xa0', ' '))
        seasons['Playoffs'].replace('nan', np.nan, inplace=True)
        seasons.set_index('Year', inplace=True)
        seasons.drop(columns={'Tm'}, inplace=True)

        return seasons

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"