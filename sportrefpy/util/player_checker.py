from typing import Union

import enchant
from enchant.pypwl import PyPWL

from sportrefpy.errors.errors import PlayerNotFoundError


class PlayerChecker:
    @staticmethod
    def is_valid_player(players: set, player: str) -> bool:
        return True if player in players else False

    # @staticmethod
    # def get_player_dictionary(players) -> Union[PyPWL, None]:
    #     # for filename in os.listdir(os.getcwd() + "/sportrefpy/assets/"):
    #     #     if sport.lower() in filename:
    #     return PyPWL(players)
    #     # return None
    #
    # @staticmethod
    # def make_suggestion(player_dict, player) -> None:
    #     try:
    #         suggestion = player_dict.suggest(player)[0]
    #         message = f"'{player}' not found. Is it possible you meant {suggestion}? Player names are case sensitive."
    #     except IndexError:
    #         message = f"'{player}' not found. Player names are case sensitive."
    #
    #     raise PlayerNotFoundError(message)
