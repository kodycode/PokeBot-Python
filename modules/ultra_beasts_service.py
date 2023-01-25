from classes import PokeBotModule
from database import UltraBeastsDAO


class UltraBeastsService(Exception):
    pass


class UltraBeastsService(PokeBotModule):
    def __init__(self) -> None:
        self.ultra_beasts_dao = UltraBeastsDAO()

    def is_pokemon_ultra_beast(self, pkmn_name: str) -> bool:
        """
        Checks to see if the pokemon is an ultra beast
        """
        try:
            if pkmn_name in self.ultra_beasts_dao.get_ultra_beasts():
                return True
            return False
        except Exception as e:
            msg = "Error has occurred in deciding if a pokemon " \
                  "was an ultra beast."
            self.post_error_log_msg(UltraBeastsService.__name__, msg, e)
