from xml.dom.pulldom import IGNORABLE_WHITESPACE
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup, Comment

from sportrefpy.nfl.league import NFL


class NFLFranchise(NFL):
    def __init__(self, franchise):
        super().__init__()
        self.abbreviation = franchise.upper()
        self.franchise_name = self.teams[franchise.lower()]['team_name']
        self.team_url = self.teams[franchise.lower()]['url']
        self.coaches_url = f'{self.team_url}coaches.htm'

    def passer_all_time_stats(self):
        '''
        Returns Pandas dataframe of all passing data.
        '''
        passing_url = f'{self.team_url}career-passing.htm'
        passing = pd.read_html(passing_url, attrs={'id': 'passing'})[0]
        passing[['W', 'L', 'T']] = passing['QBrec'].str.split('-', expand=True)
        passing.drop(columns={'Rk', 'QBrec'}, inplace=True)
        passing = passing[passing['Player'] != 'Player']
        passing.rename(columns={
            'Yds': 'Passing Yards',
            'Yds.1': 'Sacked Yards'
        }, inplace=True)
        passing.set_index('Player', inplace=True)
        passing = passing.apply(pd.to_numeric, errors='ignore')

        return passing

    def rusher_all_time_stats(self):
        '''
        Returns Pandas dataframe of all rushing data.
        '''
        rushing_url = f'{self.team_url}career-rushing.htm'
        rushing = pd.read_html(rushing_url, header=[1],
                               attrs={'id': 'rushing'})[0]
        rushing.drop(columns={'Rk'}, inplace=True)
        rushing = rushing[rushing['Player'] != 'Player']
        rushing.set_index('Player', inplace=True)
        rushing = rushing.apply(pd.to_numeric, errors='ignore')

        return rushing

    def receiving_all_time_stats(self):
        '''
        Returns Pandas dataframe of all receiving data.
        '''
        receiving_url = f'{self.team_url}career-receiving.htm'
        receiving = pd.read_html(receiving_url, attrs={'id': 'receiving'})[0]
        receiving.drop(columns={'Rk'}, inplace=True)
        receiving = receiving[receiving['Player'] != 'Player']
        receiving.set_index('Player', inplace=True)
        receiving = receiving.apply(pd.to_numeric, errors='ignore')

        return receiving

    def returns_all_time_stats(self):
        '''
        Returns Pandas dataframe of all kicking & punting return data.
        '''
        returns_url = f'{self.team_url}career-returns.htm'
        returns = pd.read_html(returns_url, header=[1],
                               attrs={'id': 'returns'})[0]
        returns.drop(columns={'Rk'}, inplace=True)
        returns = returns[returns['Player'] != 'Player']
        returns.set_index('Player', inplace=True)
        returns.rename(columns={
            'Ret': 'pRt',
            'Yds': 'pYds',
            'TD': 'pTD',
            'Lng': 'pLng',
            'Y/R': 'pY/R',
            'Rt': 'kRt',
            'Yds.1': 'kYds',
            'TD.1': 'kTD',
            'Lng.1': 'kLng',
            'Y/Rt': 'kY/R',
        }, inplace=True)
        returns = returns.apply(pd.to_numeric, errors='ignore')

        return returns

    def kicking_all_time_stats(self):
        '''
        Returns Pandas dataframe of all kicking & punting data.
        '''
        kicking_url = f'{self.team_url}career-kicking.htm'
        kicking = pd.read_html(kicking_url, attrs={'id': 'kicking'})[0]
        kicking.columns = ['Rk', 'Player', 'From', 'To', 'G', 'Pos', 'AV',
                           '0-19 FGA', '0-19 FGM', '20-29 FGA', '20-29 FGM',
                           '30-39 FGA', '30-39 FGM', '40-49 FGA', '40-49 FGM',
                           '50+ FGA', '50+ FGM', 'FGA', 'FGM', 'FG%', 'XPA',
                           'XPM', 'XP%', 'KO', 'KOYds', 'TB', 'TB%', 'KOAvg',
                           'Pnt', 'PntYds', 'PntLng', 'PntBlck', 'PntY/P']
        kicking.drop(columns={'Rk'}, inplace=True)
        kicking = kicking[kicking['Player'] != 'Player']
        kicking.set_index('Player', inplace=True)
        kicking = kicking.apply(pd.to_numeric, errors='ignore')
        kicking.fillna(0, inplace=True)

        return kicking

    def scoring_all_time_stats(self):
        '''
        Returns Pandas dataframe of all scoring data.
        '''
        scoring_url = f'{self.team_url}career-scoring.htm'
        scoring = pd.read_html(scoring_url, attrs={'id': 'scoring'})[0]
        scoring.drop(columns={'Rk'}, inplace=True)
        scoring = scoring[scoring['Player'] != 'Player']
        scoring.set_index('Player', inplace=True)
        scoring = scoring.apply(pd.to_numeric, errors='ignore')
        scoring.fillna(0, inplace=True)

        return scoring

    def defense_all_time_stats(self):
        '''
        Returns Pandas dataframe of all defense data.
        '''
        defense_url = f'{self.team_url}career-defense.htm'
        defense = pd.read_html(defense_url, header=[1],
                               attrs={'id': 'defense'})[0]
        defense.drop(columns={'Rk'}, inplace=True)
        defense = defense[defense['Player'] != 'Player']
        defense.set_index('Player', inplace=True)
        defense.rename(columns={
            'TD': 'IntTD',
            'Yds': 'IntYds',
            'TD.1': 'FmbTD',
            'Yds.1': 'FmbYds',
            'Sk': 'Sacks',
        }, inplace=True)
        defense = defense.apply(pd.to_numeric, errors='ignore')
        defense.fillna(0, inplace=True)

        return defense

    def coaches_all_time_data(self):
        '''
        Returns Pandas dataframe of all historical coach data.
        '''

        coaches = pd.read_html(self.coaches_url, header=[1],
                               attrs={'id': 'coach_sums'})[0]
        coaches['Coach'] = coaches['Coach'].apply(lambda x: x.split('+')[0])
        # coaches = coaches[coaches['Coach'] != 'Coach']
        coaches.set_index('Coach', inplace=True)
        coaches = coaches.apply(pd.to_numeric)

        return coaches

    def roster(self, year=None):
        '''
        Returns Pandas dataframe of current roster.
        '''
        if year is not None:
            roster_url = f'{self.team_url}{str(year)}_roster.htm'
            response = requests.get(roster_url)
            soup = BeautifulSoup(response.text, features='lxml')
            comments = soup.find_all(
                string=lambda text: isinstance(text, Comment))
            tables = []
            for comment in comments:
                if 'roster' in str(comment):
                    try:
                        tables.append(pd.read_html(str(comment)))
                    except:
                        continue
            roster = tables[0][0]
            roster = roster[~roster['Player'].str.contains(
                'Player|Team Total')]
            roster.set_index('Player', inplace=True)
            roster['Yrs'] = roster['Yrs'].replace('Rook', 0)
            roster.drop(columns={'AV'}, inplace=True)
            roster.rename(columns={
                'College/Univ': 'College',
                'Drafted (tm/rnd/yr)': 'Draft'}, inplace=True)
            roster['Draft'].fillna('Undrafted', inplace=True)
            return roster
        return None

    def season_history(self):
        '''
        Returns Pandas dataframe of seasons.
        '''

        seasons = pd.read_html(self.team_url, header=[1])[0]
        seasons = seasons[seasons['Tm'] != 'Tm']
        seasons = seasons[seasons['T/G'] != 'Overall Rank']
        seasons = seasons.apply(pd.to_numeric, errors='ignore')
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
        return f"<{self.abbreviation} - {self.franchise_name}>"
