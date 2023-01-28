from classes import PokeBotModule
from database import LegendaryPokemonDAO
from modules.pokebot_exceptions import LegendaryPokemonServiceException


class LegendaryPokemonService(PokeBotModule):
    def __init__(self) -> None:
        self.legendary_dao = LegendaryPokemonDAO()

    def is_pokemon_legendary(self, pkmn_name: str) -> bool:
        """
        Gives the pokemon to the trainer in their inventory
        """
        try:
            if pkmn_name in self.legendary_dao.get_legendary_pokemon():
                return True
            return False
        except Exception as e:
            msg = "Error has occurred in deciding if a pokemon " \
                  "was a legendary pokemon."
            self.post_error_log_msg(
                LegendaryPokemonServiceException.__name__,
                msg, 
                e
            )
            raise

    def get_list_of_legendary_pokemon(self) -> list:
        """
        Returns the list of legendary pokemon
        """
        try:
            return self.legendary_dao.get_legendary_pokemon()
        except Exception as e:
            msg = "Error has occurred in getting list of legendary pokemon"
            self.post_error_log_msg(
                LegendaryPokemonServiceException.__name__,
                msg, 
                e
            )
            raise       
