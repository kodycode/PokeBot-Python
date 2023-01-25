from collections import defaultdict
from classes import Pokemon
import glob
import os
import random
import re


class PokeBotAssets:
    def __init__(self, shiny=False):
        self.shiny = shiny
        self.pokemon = self._load_pokemon_imgs(shiny)

    def _load_pokemon_imgs(self, shiny: bool) -> defaultdict:
        """
        Loads pokemon images within a folder

        Note: Make path universal
        """
        filedict = defaultdict(list)
        if shiny:
            folder_path = os.path.join('assets', 'shiny')
            img_path = os.path.join('assets', 'shiny', '*.png')
        else:
            folder_path = os.path.join('assets', 'nrml')
            img_path = os.path.join('assets', 'nrml', '*.png')
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

    def get_random_pokemon_asset(self) -> Pokemon:
        """
        Gets a random pokemon from the asset folder
        """
        random_pkmn = random.choice(list(self.pokemon.keys()))
        pkmn_img_path = self.pokemon[random_pkmn][0]
        return Pokemon(
            name=random_pkmn,
            img_path=pkmn_img_path,
            is_shiny=self.shiny
        )
