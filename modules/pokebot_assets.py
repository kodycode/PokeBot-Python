from bot_logger import logger
from collections import defaultdict
from classes import PokeBotModule, Pokemon
from database import PokeballsDAO
from modules.legendary_pokemon_service import LegendaryPokemonService
from modules.pokebot_exceptions import PokeBotAssetsException
from modules.ultra_beasts_service import UltraBeastsService
import glob
import os
import random
import re


class PokeBotAssets(PokeBotModule):
    def __init__(self):
        self.legendary_service = LegendaryPokemonService()
        self.nrml_pokemon = self._load_pokemon_imgs("nrml")
        self.pokeballs = PokeballsDAO()
        self.shiny_pokemon = self._load_pokemon_imgs("shiny")
        self.ultra_service = UltraBeastsService()

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

    def get_random_pokeball_emoji(self) -> str:
        """
        Gets a random pokeball emoji to use in pokemon capture msg
        """
        try:
            return self.pokeballs.get_random_pokeball_emoji()
        except Exception as e:
            msg = "Error has occurred in getting random pokeball."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)

    def get_random_pokemon_asset(self, is_shiny: bool=False) -> Pokemon:
        """
        Gets a random pokemon from the asset folder
        """
        try:
            if is_shiny:
                random_pkmn = random.choice(list(self.shiny_pokemon.keys()))
                pkmn_img_path = self.shiny_pokemon[random_pkmn][0]
            else:
                random_pkmn = random.choice(list(self.nrml_pokemon.keys()))
                pkmn_img_path = self.nrml_pokemon[random_pkmn][0]
            is_legendary = \
                self.legendary_service.is_pokemon_legendary(random_pkmn)
            is_ultra_beast = \
                self.ultra_service.is_pokemon_ultra_beast(random_pkmn)
            return Pokemon(
                name=random_pkmn,
                img_path=pkmn_img_path,
                is_legendary=is_legendary,
                is_shiny=is_shiny,
                is_ultra_beast=is_ultra_beast,
            )
        except Exception as e:
            msg = "Error has occurred in getting random pokemon asset."
            self.post_error_log_msg(PokeBotAssetsException.__name__, msg, e)
