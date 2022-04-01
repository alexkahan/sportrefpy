# WORK IN PROGRESS

# Sports Stats
Sports stats is package that pulls data from the [Sports-Reference](https://www.sports-reference.com/) family of sites. Currently, only NBA is working but NHL, NFL, MLB, and College Basketball and Football will be supported as soon as possible.

# Installation
```bash
TBD
```

# Usage
Below are some examples for ways that you can use Sports Stats.

## Initialize a league, team, and player
```python
from sports_stats.nba.league import NBA
from sports_stats.nba.team import NBAFranchise
from sports_stats.nba.player import NBAPlayer

nba = NBA()
phi = NBAFranchise('PHI')
the_answer = NBAPlayer('Allen Iverson')
```

## Print out Franchise Codes (needed for initializing a team)
```python
from sports_stats.nba.league import NBA

nba = NBA()
nba.franchise_codes()
```

## Find the career totals (regular + playoffs) of a specific player (Pandas DataFrame)
```python
from sports_stats.nba.player import NBAPlayer

# For all stats
king = NBAPlayer('LeBron James')
king.career_totals()

# For a specific stat
beard = NBAPlayer('James Harden')
beard.career_totals()['PTS']
```

## Compare players stat totals (Pandas DataFrame)
```python
from sports_stats.nba.analysis import compare_players

showtime = compare_players(["Shaquille O'Neal", "Kobe Bryant"], 
                            stats=['PTS', 'GS']
                            total='career')
```


## Compare Franchise W/L records (Pandas DataFrame)
```python
from sports_stats.nba.analysis import compare_franchises

compare_franchises(['NYK', 'BOS'])
```

## Get stats of players/coaches for a specific Franchise (Pandas DataFrame)
```python
from sports_stats.nba.team import NBAFranchise

# Players
bulls = NBAFranchise('CHI')

# All players that have ever played for the team
bulls.players_all_time_stats()

# Or just the GOAT
bulls.players_all_time_stats('Michael Jordan')


# Coaches
spurs = NBAFranchise('SAS')

# All coaches that have ever coached the team
spurs.coaches_all_time_data()

# Or just Pop
spurs.coaches_all_time_data('Gregg Popovich')
```