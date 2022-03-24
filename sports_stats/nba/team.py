import pandas as pd
from sports_stats.nba.league import NBA

class NBAFranchise(NBA):
    def __init__(self, franchise):
        super().__init__()
        self.abbreviation = franchise
        self.franchise = self.teams[franchise]['team_name']
        self.team_url = self.teams[franchise]['url']
        self.players_url = self.team_url + 'players.html'
        self.coaches_url = self.team_url + 'coaches.html'
        self.current_roster_url = f'{self.url}/contracts/{self.abbreviation}.html'
        self.seasons_url = f'{self.url}/teams/{self.abbreviation}'

    
    def players_all_time_stats(self):
        '''
        Returns Pandas dataframe of all historical player data.
        '''

        players = pd.read_html(self.players_url)[0]
        players.columns = ['Rank', 'Player', 'From', 'To', 'Yrs', 'G', 'MP', \
            'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'TRB', 'AST', \
            'STL', 'BLK', 'TOV', 'PF', 'PTS', 'FG%', '3P%', 'FT%', 'MPG',\
            'PPG', 'RBG', 'APG']
        players.dropna(axis='rows', subset='Player', inplace=True)
        players.drop(columns={'Rank'}, inplace=True)
        players = players[players['Player'] != 'Player']
        players.set_index('Player', inplace=True)
        players = players.apply(pd.to_numeric)

        return players


    def coaches_all_time_data(self):
        '''
        Returns Pandas dataframe of all historical coach data.
        '''

        coaches = pd.read_html(self.coaches_url)[0]
        coaches.columns = ['Rank', 'Coach', 'From', 'To', 'Yrs', 'G', 'W', \
            'L', 'W/L%', 'W > .500', 'Playoffs', 'Playoff G', 'Playoff W', \
            'Playoff L', 'Playoff W/L%', 'Conf', 'Champ']
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

        current_roster = pd.read_html(self.current_roster_url)[0]
        current_roster = current_roster[current_roster.columns[:2]]
        current_roster.columns = ['Player', 'Age']
        current_roster = current_roster[current_roster['Player']\
             != 'Team Totals']
        current_roster.set_index('Player', inplace=True)
        current_roster['Age'] = current_roster['Age'].apply(lambda x: int(x))

        return current_roster

    
    def season_history(self):
        '''
        Returns Pandas dataframe of seasons.
        '''

        seasons = pd.read_html(self.seasons_url)[0]
        seasons = seasons[seasons['Team'] != 'Team']
        seasons.set_index('Season', inplace=True)
        seasons.drop(columns={'Team', 'Unnamed: 8', 'Unnamed: 15'}, 
                    inplace=True)

        return seasons
        

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"