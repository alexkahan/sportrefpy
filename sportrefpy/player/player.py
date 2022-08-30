from abc import ABC


class Player(ABC):
    def __init__(self, name: str):
        self.name = name

    @property
    def identifying_letter(self):
        raise NotImplementedError

    @property
    def players(self):
        raise NotImplementedError

    @property
    def player_url(self):
        raise NotImplementedError

    def is_valid_player(self):
        raise NotImplementedError
