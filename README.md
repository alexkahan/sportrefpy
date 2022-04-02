# WORK IN PROGRESS

# SPORTREFPY
Sportrefpy is package that pulls data from the [Sports-Reference](https://www.sports-reference.com/) family of sites. Currently, only NBA is working but NHL, NFL, MLB, and College Basketball and Football will be supported as soon as possible.

# Installation
```bash
pip install sportrefpy
```

# Usage
Below are some examples for ways that you can use Sports Stats.

## Initialize a league, team, and player
```python
from sportrefpy.nba.league import NBA
from sportrefpy.nba.team import NBAFranchise
from sportrefpy.nba.player import NBAPlayer

nba = NBA()
phi = NBAFranchise('PHI')
the_answer = NBAPlayer('Allen Iverson')
```

## Print out Franchise Codes (needed for initializing a team)
```python
from sportrefpy.nba.league import NBA

nba = NBA()
nba.franchise_codes()
```

## Find the career totals (regular + playoffs) of a specific player (Pandas DataFrame)
```python
from sportrefpy.nba.player import NBAPlayer

# For all stats
king = NBAPlayer('LeBron James')
king.career_totals()

# For a specific stat
beard = NBAPlayer('James Harden')
beard.career_totals()['PTS']
```

## Compare players stat totals (Pandas DataFrame)
```python
from sportrefpy.nba.analysis import compare_players

showtime = compare_players(["Shaquille O'Neal", "Kobe Bryant"], 
                            stats=['PTS', 'GS']
                            total='career')
```
- _stats_ must be a list, with as many stats as you'd like. Required.
- _total_ defaults to 'career', but can also be 'post' or 'reg'.


## Compare Franchise W/L records (Pandas DataFrame)
```python
from sportrefpy.nba.analysis import compare_franchises

compare_franchises(['NYK', 'BOS'])
```
- must be a list of teams, even if only using 1.

## Get stats of players/coaches for a specific Franchise (Pandas DataFrame)
```python
from sportrefpy.nba.team import NBAFranchise

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

## Get roster for a given season (Pandas DataFrame)
```python
from sportrefpy.nba.team import NBAFranchise

warriors = NBAFranchise('GSW')
warriors.roster(2016)
```
- use the integer for the year the season ends in. This example returns the 2015-16 Golden State Warriors.