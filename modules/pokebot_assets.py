from bot_logger import logger
from collections import defaultdict
from classes import PokeBotModule, Pokemon
from database import PokeballsDAO
from modules.legendary_pokemon_service import LegendaryPokemonService
from modules.pokebot_exceptions import PokeBotAssetsException
from modules.ultra_beasts_service import UltraBeastsService
from utils import remove_shiny_pokemon_name
import copy
import glob
import os
import random
import re


class PokeBotAssets(PokeBotModule):
    """
    Handles all pokemon related assets
    """

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

    SHINY_PREFIX = "(shiny)"

    def __init__(self):
        self.legendary_service = LegendaryPokemonService()
        self.nrml_pokemon = self._load_pokemon_imgs("nrml")
        self.pokeballs = PokeballsDAO()
        self.shiny_pokemon = self._load_pokemon_imgs("shiny")
        self.ultra_service = UltraBeastsService()
        self.bronze_lootbox_pokemon = self._load_bronze_lootbox_pokemon()
        self.silver_lootbox_pokemon = self._load_silver_lootbox_pokemon()
        self.gold_lootbox_pokemon = self._load_gold_lootbox_pokemon()

    def _load_bronze_lootbox_pokemon(self) -> set:
        """
        Loads the pool of bronze lootbox pokemon
        """
        try:
            bronze_lootbox_pokemon = set(self.nrml_pokemon.keys())
            legendary_pkmn = \
                self.legendary_service.get_list_of_legendary_pokemon()
            ultra_beasts = \
                self.ultra_service.get_list_of_ultra_beasts()
            for pkmn in legendary_pkmn:
                bronze_lootbox_pokemon.remove(pkmn)
            for beast in ultra_beasts:
                bronze_lootbox_pokemon.remove(beast)
            return bronze_lootbox_pokemon
        except Exception as e:
            msg = "Error has occurred loading bronze lootbox pokemon."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)
            raise

    def _load_silver_lootbox_pokemon(self) -> set:
        """
        Loads the pool of silver lootbox pokemon
        """
        try:
            silver_lootbox_pokemon = set(self.nrml_pokemon.keys())
            return silver_lootbox_pokemon
        except Exception as e:
            msg = "Error has occurred loading silver lootbox pokemon."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)
            raise

    def _load_gold_lootbox_pokemon(self) -> set:
        """
        Loads the pool of gold lootbox pokemon
        """
        try:
            legendary_pkmn = \
                self.legendary_service.get_list_of_legendary_pokemon()
            ultra_beasts = \
                self.ultra_service.get_list_of_ultra_beasts()
            gold_lootbox_pokemon = set(legendary_pkmn).union(set(ultra_beasts))
            return gold_lootbox_pokemon
        except Exception as e:
            msg = "Error has occurred loading gold lootbox pokemon."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)
            raise

    def _load_pokemon_imgs(self, pkmn_type: str) -> defaultdict:
        """
        Loads pokemon images within a folder

        Note: Make path universal
        """
        try:
            filedict = defaultdict(list)
            folder_path = os.path.join('assets', pkmn_type)
            img_path = os.path.join('assets', pkmn_type, '*.png')
            for filename in glob.glob(img_path):
                result = re.match(r'([^\d]+)', filename)
                if result:
                    pkmn_name = filename.lower()
                    pkmn_name = pkmn_name.replace(folder_path, "")
                    pkmn_name = pkmn_name.replace('/', "")
                    pkmn_name = pkmn_name.replace('\\', "")
                    pkmn_name = pkmn_name.replace('.png', "")
                    filedict[pkmn_name].append(filename)
            return filedict
        except Exception as e:
            msg = "Error has occurred loading pokemon images."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)
            raise

    def get_random_pokeball_emoji(self) -> str:
        """
        Gets a random pokeball emoji to use in pokemon capture msg
        """
        try:
            return self.pokeballs.get_random_pokeball_emoji()
        except Exception as e:
            msg = "Error has occurred in getting random pokeball."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)
            raise

    def get_lootbox_pokemon_asset(
        self,
        is_shiny: bool,
        lootbox: str
    ) -> Pokemon:
        """
        Gets a random pokemon from the asset folder
        """
        try:
            lootbox_pkmn = set()
            if lootbox == self.BRONZE:
                lootbox_pkmn = self.bronze_lootbox_pokemon
            elif lootbox == self.SILVER:
                lootbox_pkmn = self.silver_lootbox_pokemon
            elif lootbox == self.GOLD:
                lootbox_pkmn = self.gold_lootbox_pokemon
            pkmn_name = random.sample(lootbox_pkmn, 1)[0]
            return self.get_pokemon_asset(pkmn_name, is_shiny)
        except Exception as e:
            msg = "Error has occurred in getting random pokemon asset."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)
            raise

    def get_random_pokemon_asset(self, is_shiny: bool=False) -> Pokemon:
        """
        Gets a random pokemon from the asset folder
        """
        try:
            is_egg = False
            if is_shiny:
                random_pkmn = random.choice(list(self.shiny_pokemon.keys()))
                pkmn_img_path = self.shiny_pokemon[random_pkmn][0]
            else:
                random_pkmn = random.choice(list(self.nrml_pokemon.keys()))
                pkmn_img_path = self.nrml_pokemon[random_pkmn][0]
            if random_pkmn == "egg" or random_pkmn == "egg-manaphy":
                is_egg = True
            is_legendary = \
                self.legendary_service.is_pokemon_legendary(random_pkmn)
            is_ultra_beast = \
                self.ultra_service.is_pokemon_ultra_beast(random_pkmn)
            return Pokemon(
                name=random_pkmn,
                img_path=pkmn_img_path,
                is_egg=is_egg,
                is_legendary=is_legendary,
                is_shiny=is_shiny,
                is_ultra_beast=is_ultra_beast,
            )
        except Exception as e:
            msg = "Error has occurred in getting random pokemon asset."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)
            raise

    def get_pokemon_asset(
        self,
        pkmn_name: str,
        is_shiny: bool=False
    ) -> Pokemon:
        """
        Gets a specific pokemon from the asset folder
        """
        try:
            is_egg = False
            if is_shiny:
                pkmn_img_path = self.shiny_pokemon[pkmn_name][0]
            else:
                pkmn_img_path = self.nrml_pokemon[pkmn_name][0]
            if pkmn_name == "egg" or pkmn_name == "egg-manaphy":
                is_egg = True
            is_legendary = \
                self.legendary_service.is_pokemon_legendary(pkmn_name)
            is_ultra_beast = \
                self.ultra_service.is_pokemon_ultra_beast(pkmn_name)
            return Pokemon(
                name=pkmn_name,
                img_path=pkmn_img_path,
                is_egg=is_egg,
                is_legendary=is_legendary,
                is_shiny=is_shiny,
                is_ultra_beast=is_ultra_beast,
            )
        except Exception as e:
            msg = "Error has occurred in getting specified pokemon asset."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)
            raise
