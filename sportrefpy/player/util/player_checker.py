class PlayerChecker:
    @staticmethod
    def is_valid_player(players: set, player: str) -> bool:
        return True if player in players else False
