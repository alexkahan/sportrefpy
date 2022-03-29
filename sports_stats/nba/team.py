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

    
    def players_all_time_stats(self, player=None):
        '''
        Returns Pandas dataframe of all historical player data for that team.
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

        if player is not None:
            try:
                return players.loc[player]
            except KeyError:
                return 'Player not found.'

        return players


    def coaches_all_time_data(self, coach=None):
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

        if coach is not None:
            try:
                return coaches.loc[coach]
            except KeyError:
                return 'Coach not found.'

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

    
    def season_history(self, year=None):
        '''
        Returns Pandas dataframe of seasons.
        '''

        seasons = pd.read_html(self.seasons_url)[0]
        seasons = seasons[seasons['Team'] != 'Team']
        seasons.set_index('Season', inplace=True)
        seasons['Team'] = seasons['Team'].apply(lambda x: x.split('*')[0])
        seasons.drop(columns={'Unnamed: 8', 'Unnamed: 15'}, 
                    inplace=True)

        if year is not None:
            try:
                return seasons.loc[year]
            except KeyError:
                return 'Season not found.'

        return seasons
        

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"