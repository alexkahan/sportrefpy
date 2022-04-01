import os

from sports_stats.nba.league import NBA
from sports_stats.nba.team import NBAFranchise

def all_players():
        players = set()
        nba = NBA()
        for team in nba.teams.keys():
            franchise = NBAFranchise(team)
            players.update(franchise.players_all_time_stats().index)
        with open('sports_stats/assets/nba_players.txt', 'w', errors='ignore') as file:
            for player in players:
                file.write(f'{player}\n')

def spellcheck():
    if not os.path.exists('sports_stats/assets/nba_players.txt'):
            all_players()