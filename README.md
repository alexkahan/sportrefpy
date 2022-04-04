# SPORTREFPY
Sportrefpy is package that pulls data from the [Sports-Reference](https://www.sports-reference.com/) family of sites. Currently, only the NBA and NHL are working but NFL, MLB, and College Basketball and Football will be supported as soon as possible.

# Table of Contents
- [Installation](#installation)
- [Usage](#usage)
    - [NBA](#nba)
	    - [Initialize league, team, or player](#initialize-a-league-team-or-player)
        - [Find Franchise Codes](#print-out-franchise-codes-needed-for-initializing-a-team)
        - [Career Totals](#find-the-career-totals-regular--playoffs-of-a-specific-player)
        - [Compare Players](#compare-players-stat-totals)
        - [Compare Franchises](#compare-franchise-wl-records)
        - [Team-specific Player Stats](#get-stats-of-players-for-a-specific-franchise)
        - [Team-specific Coach Stats](#get-stats-of-coaches-for-a-specific-franchise)
        - [Roster](#get-roster-for-a-given-season)
        - [Current Season Standings](#get-current-season-standings-by-conference)
        - [Get Franchise Season History](#get-franchise-season-history)
        - [Find which seasons a team won the NBA Finals](#find-which-seasons-a-team-won-the-nba-finals)
    - [NHL](#nhl)
	    - [Initialize a league, team, or player](#initialize-a-league-team-or-player-1)
        - [Find Franchise Codes](#print-out-franchise-codes-needed-for-initializing-a-team-1)
        - [Compare Franchises](#compare-franchise-wl-records-1)
        - [Roster](#get-roster-for-a-given-season-1)
        - [Current Season Standings](#get-current-season-standings-by-conference-1)
        - [Get Franchise Season History](#get-franchise-season-history-1)
        - [Get Stanley Cup winning seasons](#get-stanley-cup-winning-seasons)
    - [NFL](#nfl)
	    - [Initialize a league, team, or player](#initialize-a-league-team-or-player-2)
        - [Find Franchise Codes](#print-out-franchise-codes-needed-for-initializing-a-team-2)
        - [Conference Standings](#get-conference-standings-by-season)
    - [Saving Data](#saving-data)


# Installation
```bash
pip install sportrefpy
```

# Usage
Each league is more or less set up the same, but they do have some slight differences.
Below are some examples for ways that you can use sportrefpy for each sport.

## NBA

### Initialize a league, team, or player
```python
from sportrefpy.nba.league import NBA
from sportrefpy.nba.team import NBAFranchise
from sportrefpy.nba.player import NBAPlayer

nba = NBA()
sixers = NBAFranchise('PHI')
the_answer = NBAPlayer('Allen Iverson')
```

### Print out Franchise Codes (needed for initializing a team)
```python
from sportrefpy.nba.league import NBA

nba = NBA()
nba.franchise_codes()
```

### Find the career totals (regular + playoffs) of a specific player
```python
from sportrefpy.nba.player import NBAPlayer

# For all stats
king = NBAPlayer('LeBron James')
king.career_totals()

# For a specific stats
beard = NBAPlayer('James Harden')
beard.career_totals(stats=['PTS', 'G'])
```
- _stats_ is None by default. If provided, it must be a list even if only using 1.

### Compare players stat totals
```python
from sportrefpy.nba.analysis import compare_players

showtime = compare_players(["Shaquille O'Neal", "Kobe Bryant"], 
                            stats=['PTS', 'TRB'],
                            total='career')
```
- _stats_ must be a list, with as many stats as you'd like. Required.
- _total_ defaults to 'career', but can also be 'post' or 'reg'.


### Compare Franchise W/L records
```python
from sportrefpy.nba.analysis import compare_franchises

compare_franchises(['NYK', 'BOS'])
```
- must be a list of teams, even if only using 1.

### Get stats of players for a specific Franchise
```python
from sportrefpy.nba.team import NBAFranchise

bulls = NBAFranchise('CHI')

# All players that have ever played for the team
bulls.players_all_time_stats()

# Or just the GOAT
bulls.players_all_time_stats('Michael Jordan')
```

### Get stats of coaches for a specific Franchise
```python
from sportrefpy.nba.team import NBAFranchise

spurs = NBAFranchise('SAS')

# All coaches that have ever coached the team
spurs.coaches_all_time_data()

# Or just Pop
spurs.coaches_all_time_data('Gregg Popovich')
```

### Get roster for a given season
```python
from sportrefpy.nba.team import NBAFranchise

warriors = NBAFranchise('GSW')
warriors.roster(2016)
```
- use integer year that season ends in. This example returns the 2015-16 Golden State Warriors.


### Get current season standings by conference
```python
from sportrefpy.nba.league import NBA

nba = NBA()

# Both conferences
east, west = nba.conference_standings()

# Just one of them
west = nba.conference_standings(conf='west')
east = nba.conference_standings(conf='east')
```


### Get franchise season history
```python
from sportrefpy.nba.team import NBAFranchise

mavs = NBAFranchise('DAL')

# Get all seasons
mavs.season_history()

# Get an individual season
mavs.season_history(year='2010-11')
```
 - _year_ defaults to all seasons. For an individual season, it needs to be a string like in the above example.


### Find which seasons a team won the NBA Finals
```python
from sportrefpy.nba.team import NBAFranchise

pistons = NHLFranchise('DET')
seasons = pistons.season_history()
seasons[seasons['Playoffs']  == 'Won Finals']]
```

## NHL

### Initialize a league, team, or player
```python
from sportrefpy.nhl.league import NHL
from sportrefpy.nhl.team import NHLFranchise
from sportrefpy.nhl.player import NHLPlayer

nhl = NHL()
flyers = NHL('PHI')
the_great_one = NHL('Wayne Gretzky')
```

### Print out Franchise Codes (needed for initializing a team)
```python
from sportrefpy.nhl.league import NHL

nhl = NHL()
nhl.franchise_codes()
```

### Compare Franchise W/L records
```python
from sportrefpy.nhl.analysis import compare_franchises

compare_franchises(['TBL', 'DET'])
```
- must be a list of teams, even if only using 1.


### Get roster for a given season
```python
from sportrefpy.nhl.team import NHLFranchise

blues = NHLFranchise('STL')
blues.roster(2019)
```
- use integer year that season ends in. This example returns the 2018-19 St. Louis Blues.

### Get current season standings by conference
```python
from sportrefpy.nhl.league import NHL

nhl = NHL()

# Both conferences
east, west = nhl.conference_standings()

# Just one of them
west = nhl.conference_standings(conf='west')
east = nhl.conference_standings(conf='east')
```

### Get franchise season history
```python
from sportrefpy.nhl.team import NHLFranchise

flames = NHLFranchise('CGY')

# Get all seasons
flames.season_history()

# Get an individual season
flames.season_history(year='1988-89')
```
 - _year_ defaults to all seasons. For an individual season, it needs to be a string like in the above example.


### Get Stanley Cup winning seasons
```python
from sportrefpy.nhl.team import NHLFranchise

leafs = NHLFranchise('TOR')
seasons = leafs.season_history()
seasons[seasons['Playoffs']  == 'Won Stanley Cup Final']]
```


## NFL

### Initialize a league, team, or player
```python
from sportrefpy.nfl.league import NFL
from sportrefpy.nfl.team import NFLFranchise
from sportrefpy.nfl.player import NFLPlayer

nfl = NFL()
sixers = NFLFranchise('PHI')
the_answer = NFLPlayer('Allen Iverson')
```

### Print out Franchise Codes (needed for initializing a team)
```python
from sportrefpy.nfl.league import NFL

nfl = NFL()
nfl.franchise_codes()
```

### Get conference standings by season
```python
from sportrefpy.nfl.league import NFL

nfl = NFL()

# Both conferences
afc, nfc = nhl.conference_standings()

# Just one of them
nfc = nhl.conference_standings(conf='NFC')
afc = nhl.conference_standings(conf='AFC')
```

## Saving Data

You can write the data to a CSV, JSON, or other file just like you would a Pandas DataFrame

```python
import pandas as pd
from sportrefpy.nba.analysis import compare_franchises

compare_franchises(['IND', 'MIL']).to_csv('comparison.csv')
```