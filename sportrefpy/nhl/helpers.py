import os

from sportrefpy.nhl.league import NHL
from sportrefpy.nhl.team import NHLFranchise

def all_players():
        players = set()
        nhl = NHL()
        for team in nhl.teams.keys():
            franchise = NHLFranchise(team)
            players.update(franchise.skaters_all_time_stats().index)
            players.update(franchise.goalies_all_time_stats().index)
        with open(os.path.dirname(os.path.dirname(__file__)) + '\\assets\\nhl_players.txt', 'w', encoding='ascii') as file:
            for player in players:
                try:
                    player = player.replace('*', '')
                    file.write(f'{player}\n')
                except UnicodeEncodeError:
                    continue