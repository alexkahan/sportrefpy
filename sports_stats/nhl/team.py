from sports_stats.nhl.league import NHL

class NHLFranchise(NHL):
    def __init__(self, franchise):
        super().__init__()
        self.abbreviation = franchise
        self.franchise = self.teams[franchise]['team_name']
        self.team_url = self.teams[franchise]['url']

    def __repr__(self):
        return f"<{self.abbreviation} - {self.franchise}>"