from sports_stats.nfl.league import NFL

class NFLFranchise(NFL):
    def __init__(self, franchise):
        super().__init__()
        self.abbreviation = franchise.upper()
        self.franchise = self.teams[franchise]['team_name']
        self.team_url = self.teams[franchise]['url']

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"