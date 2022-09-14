# SPORTREFPY
Sportrefpy is package that pulls data from the [Sports-Reference](https://www.sports-reference.com/) family of sites.

# Installation
```bash
pip install sportrefpy
```

# Basic Usage
```python
from sportrefpy.nba.league import NBA
from sportrefpy.nba.player import NBAPlayer
from sportrefpy.nba.team import NBATeam

# Instantiate a league, player, or team
nba = NBA()
allen_iverson = NBAPlayer('Allen Iverson')
sixers = NBATeam('PHI')

# Get stuff
nba.compare_players(['LeBron James', 'Kobe Bryant'])
allen_iverson.accolades()
sixers.roster(2022)
```
More in-depth usage can be found in the [docs](#).
