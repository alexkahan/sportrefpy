from sports_stats.nhl.league import NHL
import pandas as pd
import numpy as np

class NHLFranchise(NHL):
    def __init__(self, franchise):
        super().__init__()
        self.abbreviation = franchise
        self.franchise = self.teams[franchise]['team_name']
        self.team_url = self.teams[franchise]['url']
        self.skaters_url = self.team_url.replace('history', 'skaters')
        self.goalies_url = self.team_url.replace('history', 'goalies')
        self.coaches_url = self.team_url.replace('history', 'coaches')
        self.current_roster_url = self.team_url.replace('history.html', '')

    
    def skaters_all_time_stats(self):
        '''
        Returns Pandas dataframe of all historical player data.
        '''

        players = pd.read_html(self.skaters_url)[0]
        players.columns = ['Rank', 'Player', 'From', 'To', 'Yrs', 'GP', 'G', \
            'A', 'PTS', '+/-', 'PIM', 'EVG', 'PPG', 'SHG', 'GWG', 'EVA', \
            'PPA', 'SHA', 'S', 'S%', 'TOI', 'ATOI']
        players.dropna(axis='rows', subset='Player', inplace=True)
        players.drop(columns={'Rank', 'ATOI'}, inplace=True)
        players = players[players['Player'] != 'Player']
        players.set_index('Player', inplace=True)
        players = players.apply(pd.to_numeric)
        
        return players

    def goalies_all_time_stats(self):
        '''
        Returns Pandas dataframe of all historical player data.
        '''

        goalies = pd.read_html(self.goalies_url)[0]
        goalies.columns = ['Rank', 'Player', 'From', 'To', 'Yrs', 'GP', 'GS', \
            'W', 'L', 'T/O', 'GA', 'SA', 'SV', 'SV%', 'GAA', 'SO', \
            'MIN', 'QS', 'QS%', 'RBS', 'GA%-', 'GSAA', 'G', 'A', 'PTS', 'PIM']
        goalies.dropna(axis='rows', subset='Player', inplace=True)
        goalies.drop(columns={'Rank'}, inplace=True)
        goalies = goalies[goalies['Player'] != 'Player']
        goalies.set_index('Player', inplace=True)
        goalies = goalies.apply(pd.to_numeric)
        
        return goalies


    def coaches_all_time_data(self):
        '''
        Returns Pandas dataframe of all historical coach data.
        '''

        coaches = pd.read_html(self.coaches_url, header=[1])[0]
        coaches.columns = ['Rank', 'Coach', 'From', 'To', 'Yrs', 'G', 'W', \
            'L', 'T', 'OL', 'PTS', 'PTS%', 'Playoff G', 'Playoff W', \
            'Playoff L', 'Playoff T', 'Playoff W-L%']
        coaches.dropna(axis='rows', subset='Coach', inplace=True)
        coaches.drop(columns={'Rank'}, inplace=True)
        coaches = coaches[coaches['Coach'] != 'Coach']
        coaches.set_index('Coach', inplace=True)
        coaches = coaches.apply(pd.to_numeric)

        return coaches


    def current_roster(self):
        '''
        Returns Pandas dataframe of current roster.
        '''

        current_roster = pd.read_html(self.current_roster_url)[3]
        current_roster['Player'] = current_roster['Player']\
            .apply(lambda x: x.split('(C)')[0].strip())
        current_roster.set_index('Player', inplace=True)
        current_roster = current_roster[['Pos', 'Age', 'Ht', 'Wt']]
        current_roster.rename(columns={
            'Pos':'Position',
            'Ht': 'Height',
            'Wt': 'Weight'
        }, inplace=True)
        current_roster['Age'] = current_roster['Age'].apply(lambda x: int(x))
        current_roster['Weight'] = current_roster['Weight'].\
            apply(lambda x: int(x))

        return current_roster

    
    def season_history(self):
        '''
        Returns Pandas dataframe of seasons.
        '''

        seasons = pd.read_html(self.team_url)[0]
        seasons = seasons[seasons['Team'] != 'Team']
        seasons.set_index('Season', inplace=True)
        seasons.drop(columns={'Lg', 'Team'}, 
                    inplace=True)

        return seasons

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"