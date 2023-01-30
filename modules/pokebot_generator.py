from classes import Pokemon, PokeBotModule
from modules.pokebot_assets import PokeBotAssets
from modules.pokebot_rates import PokeBotRates
from modules.pokebot_exceptions import PokeBotGeneratorException
import random


class PokeBotGenerator(PokeBotModule):

    def __init__(self, assets: PokeBotAssets, rates: PokeBotRates):
        self.assets = assets
        self.rates = rates

    def generate_random_pokemon(
        self,
        is_shiny: bool=False,
        is_egg: bool=False,
        is_night_vendor_generated: bool=False,
        lootbox: str=''
    ) -> Pokemon:
        """
        Generates a random pokemon and returns a Pokemon object
        """
        try:
            is_shiny_pokemon = is_shiny
            if not is_shiny:
                is_shiny_pokemon = self._determine_shiny_pokemon(
                    is_egg,
                    is_night_vendor_generated
                )
            if lootbox:
                pkmn = self.assets.get_lootbox_pokemon_asset(
                    is_shiny_pokemon,
                    lootbox
                )
            else:
                pkmn = self.assets.get_random_pokemon_asset(
                    is_shiny=is_shiny_pokemon
                )
            return pkmn
        except Exception as e:
            msg = "Error has occurred in generating pokemon."
            self.post_error_log_msg(PokeBotGeneratorException.__name__, msg, e)
            raise

    def _determine_shiny_pokemon(
        self,
        is_egg: bool,
        is_night_vendor_generated: bool
    ) -> bool:
        """
        Determines the odds of a shiny pokemon 
        """
        try:
            shiny_catch_rate = -1
            shiny_rng_chance = random.uniform(0, 1)
            if is_night_vendor_generated:
                shiny_catch_rate = self.rates.get_shiny_pkmn_night_vendor_rate()
            elif is_egg:
                shiny_catch_rate = self.rates.get_shiny_pkmn_hatch_multiplier()
            else:
                shiny_catch_rate = self.rates.get_shiny_pkmn_catch_rate()
            if shiny_rng_chance < shiny_catch_rate:
                return True
            return False
        except Exception as e:
            msg = "Error has occurred in determining shiny pokemon."
            self.post_error_log_msg(PokeBotGeneratorException.__name__, msg, e)
            raise

    def generate_pokemon(self, pkmn_name: str, is_egg=False) -> Pokemon:
        """
        Generates a specified pokemon and returns a Pokemon object
        """
        try:
            is_shiny_pokemon = self._determine_shiny_pokemon(is_egg)
            if is_shiny_pokemon:
                pkmn = self.assets.get_pokemon_asset(pkmn_name, is_shiny=True)
            else:
                pkmn = self.assets.get_pokemon_asset(pkmn_name)
            return pkmn
        except Exception as e:
            msg = "Error has occurred in generating specific pokemon."
            self.post_error_log_msg(PokeBotGeneratorException.__name__, msg, e)
            raise

    def generate_lootbox(self, daily=False) -> str:
        """
        Generates a lootbox with consideration into daily or catch rates
        """
        try:
            lootbox_rng = random.uniform(0, 1)
            if daily:
                lootbox_bronze_rate = \
                    self.rates.get_daily_lootbox_bronze_rate()
                lootbox_silver_rate = \
                    self.rates.get_daily_lootbox_silver_rate()
                lootbox_gold_rate = \
                    self.rates.get_daily_lootbox_gold_rate()
            else:
                lootbox_bronze_rate = \
                    self.rates.get_lootbox_bronze_rate()
                lootbox_silver_rate = \
                    self.rates.get_lootbox_silver_rate()
                lootbox_gold_rate = \
                    self.rates.get_lootbox_gold_rate()
            if lootbox_rng < lootbox_gold_rate:
                return "gold"
            elif lootbox_rng < lootbox_silver_rate:
                return "silver"
            elif lootbox_rng < lootbox_bronze_rate:
                return "bronze"
            return None
        except Exception as e:
            msg = "Error has occurred in generating lootbox."
            self.post_error_log_msg(PokeBotGeneratorException.__name__, msg, e)
            raise

