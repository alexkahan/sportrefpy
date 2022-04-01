from sports_stats.nba.league import NBA
from sports_stats.nba.team import NBAFranchise

def all_players():
        players = set()
        nba = NBA()
        for team in nba.teams.keys():
            franchise = NBAFranchise(team)
            players.update(franchise.players_all_time_stats().index)
        with open('sports_stats/assets/nba_players.txt', 'w', encoding='ascii') as file:
            for player in players:
                try:
                    file.write(f'{player}\n')
                except UnicodeEncodeError:
                    continue