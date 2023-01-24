from bot_logger import logger
from classes import Pokemon
from database import LegendaryPokemonDAO, ShinyPokemonRatesDAO, UltraBeastsDAO
from modules import PokeBotRates
from modules.pokebot_trainer_service import PokeBotTrainerService
from utils import get_ctx_user_id
import random
import time


class PokeBotLogicException(Exception):
    pass


class PokeBotLogic:
    """Handles the basic logic of features for PokeBot"""

    def __init__(self):
        self.pokebot_rates = PokeBotRates()
        self.legendary_pkmn = LegendaryPokemonDAO()
        self.shiny_pkmn = ShinyPokemonRatesDAO()
        self.trainer_service = PokeBotTrainerService()
        self.ultra_beasts = UltraBeastsDAO()

    async def catch_pokemon(self, ctx):
        """
        Generates a random pokemon to be caught
        """
        try:
            current_time = time.time()
            user_id = get_ctx_user_id(ctx)
            is_trainer_catching = self.trainer_service.validate_trainer_catch(user_id)
            if is_trainer_catching:
                random_pkmnball = random.choice(list(self.pokeball))
                random_pkmn = self._generate_random_pokemon()
                self.trainer_service.give_pokemon_to_trainer(
                    random_pkmn.name,
                    user_id
                )
                self.trainer_service.validate_trainer_catch()
                trainer_profile["last_catch_time"] = current_time
                lootbox = self._generate_lootbox(trainer_profile)
                self._move_pokemon_to_inventory(trainer_profile,
                                                random_pkmn,
                                                is_shiny)
                self._save_trainer_file(self.trainer_data)
                await self._display_total_pokemon_caught()
                await self._post_pokemon_catch(ctx,
                                               random_pkmn,
                                               pkmn_img_path,
                                               random_pkmnball,
                                               is_shiny,
                                               "caught",
                                               lootbox)
        except Exception as e:
            print("An error has occured in catching pokemon. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _generate_random_pokemon(self) -> Pokemon:
        """
        Generates a random pokemon and returns a tuple of the
        pokemon name, image path, and whether the pokemon is shiny
        or not
        """
        is_shiny_pokemon = self._determine_shiny_pokemon()
        if is_shiny_pokemon:
            random_pkmn = random.choice(list(self.shiny_pokemon.keys()))
            pkmn_img_path = self.shiny_pokemon[random_pkmn][0]
        else:
            random_pkmn = random.choice(list(self.nrml_pokemon.keys()))
            pkmn_img_path = self.nrml_pokemon[random_pkmn][0]
        return Pokemon(
            pkmn_name=random_pkmn,
            img_path=pkmn_img_path,
            is_shiny=is_shiny_pokemon
        )

    def _determine_shiny_pokemon(self) -> bool:
        """
        Determines the odds of a shiny pokemon 
        """
        shiny_rng_chance = random.uniform(0, 1)
        if shiny_rng_chance < self.pokebot_rates.get_shiny_pkmn_catch_rate():
            return True
        return False
