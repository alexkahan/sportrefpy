import pandas as pd
import numpy as np

from sportrefpy.nfl.league import NFL


class NFLFranchise(NFL):
    def __init__(self, franchise):
        super().__init__()
        self.abbreviation = franchise.upper()
        self.franchise = self.teams[franchise.lower()]['team_name']
        self.team_url = self.teams[franchise.lower()]['url']
        self.coaches_url = f'{self.team_url}coaches.htm'
    
    # def players_all_time_stats(self):
    #     '''
    #     Returns Pandas dataframe of all historical player data.
    #     '''

    #     players = pd.read_html(self.players_url)[0]
    #     players.columns = ['Rank', 'Player', 'From', 'To', 'Yrs', 'G', 'MP', \
    #         'FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'TRB', 'AST', \
    #         'STL', 'BLK', 'TOV', 'PF', 'PTS', 'FG%', '3P%', 'FT%', 'MPG',\
    #         'PPG', 'RBG', 'APG']
    #     players.dropna(axis='rows', subset='Player', inplace=True)
    #     players.drop(columns={'Rank'}, inplace=True)
    #     players = players[players['Player'] != 'Player']
    #     players.set_index('Player', inplace=True)
    #     players = players.apply(pd.to_numeric)

    #     return players


    def coaches_all_time_data(self):
        '''
        Returns Pandas dataframe of all historical coach data.
        '''

        coaches = pd.read_html(self.coaches_url, header=[1], attrs={'id': 'coach_sums'})[0]
        coaches['Coach'] = coaches['Coach'].apply(lambda x: x.split('+')[0])
        # coaches = coaches[coaches['Coach'] != 'Coach']
        coaches.set_index('Coach', inplace=True)
        coaches = coaches.apply(pd.to_numeric)

        return coaches


    # def roster(self, year=None):
    #     '''
    #     Returns Pandas dataframe of current roster.
    #     '''
    #     roster_url = f'{self.team_url}{str(year)}_roster.htm'
    #     r = requests.get(roster_url)
    #     soup = BeautifulSoup(r.content, 'html.parser')

    #     for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
    #         if comment.find("<table ") > 0:
    #             comment_soup = BeautifulSoup(comment, 'html.parser')
    #             table = comment_soup.find("table")
    #             print(table.string)
        

        # roster = roster[roster['Player']!= 'Player']
        # roster.set_index('Player', inplace=True)
        # roster['Yrs'] = roster['Years'].replace('Rook', 0)
        # return roster

    
    def season_history(self):
        '''
        Returns Pandas dataframe of seasons.
        '''

        seasons = pd.read_html(self.team_url, header=[1])[0]
        seasons = seasons[seasons['Tm'] != 'Tm']
        seasons = seasons[seasons['T/G'] != 'Overall Rank']
        seasons['Year'] = seasons['Year'].astype(int)
        seasons.rename(columns={
            'Coaches': 'Head Coach',
            'AV': 'Top Approximate Value',
            'Passer': 'Top Passer',
            'Rusher': 'Top Rusher',
            'Receiver': 'Top Receiver'
        }, inplace=True)
        seasons.set_index('Year', inplace=True)
        seasons.drop(columns={'Tm', 'Pts', 'Yds', 'Yds.1', 'Pts.1', 'Pts±',
                            'Yds±', 'out of', 'MoV', 'SoS', 'SRS', 'OSRS', 
                            'DSRS'}, inplace=True)

        return seasons
        

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"