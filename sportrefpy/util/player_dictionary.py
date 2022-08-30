import os
from typing import Union

import enchant
from enchant import PyPWL

from sportrefpy.errors.errors import PlayerNotFoundError
from sportrefpy.errors.not_found import PlayerNotFound


class PlayerDictionary:
    @staticmethod
    def get_player_dictionary(sport) -> Union[PyPWL, None]:
        for filename in os.listdir(os.getcwd() + "/sportrefpy/assets/"):
            if sport.lower() in filename:
                return enchant.PyPWL(
                    f"{os.path.dirname(os.path.dirname(__file__))}/assets/{filename}"
                )
        return None

    @staticmethod
    def make_suggestion(player_dict, player) -> None:
        try:
            suggestion = player_dict.suggest(player)[0]
            message = f"'{player}' not found. Is it possible you meant {suggestion}? Player names are case sensitive."
        except IndexError:
            message = f"'{player}' not found. Player names are case sensitive."

        raise PlayerNotFoundError(message)
