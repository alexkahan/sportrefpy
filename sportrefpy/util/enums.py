import enum


class SportEnum(enum.Enum):
    NBA = "NBA"
    NHL = "NHL"
    NFL = "NFL"
    MLB = "MLB"
    CBB = "CBB"
    CFB = "CFB"


class NumTeams(enum.IntEnum):
    NBA = 30
    NHL = 32
    NFL = 32
    MLB = 30
    CBB = 600
    CFB = 600


class SportURLs(enum.Enum):
    NBA = "https://www.basketball-reference.com"
    NHL = "https://www.hockey-reference.com"
    NFL = "https://www.pro-football-reference.com"
    MLB = "https://www.baseball-reference.com"
    CBB = "https://www.sports-reference.com/cbb"
    CFB = "https://www.sports-reference.com/cfb"


class BoxScoreURLs(enum.Enum):
    NBA = f"{SportURLs.NBA.value}/boxscores/"
    NHL = f"{SportURLs.NHL.value}/boxscores/"
    NFL = f"{SportURLs.NFL.value}/boxscores/"
    MLB = f"{SportURLs.MLB.value}/boxes/"
    CBB = f"{SportURLs.CBB.value}/boxscores/"
    CFB = f"{SportURLs.CFB.value}/boxscores/"
