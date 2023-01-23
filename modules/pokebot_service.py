from database import LegendaryPokemonDAO, ShinyPokemonRatesDAO, TrainerDAO, UltraBeastsDAO


class PokeBotLogic:
    """Handles the basic logic of features for PokeBot"""
    def __init__(self):
        self.legendary_pkmn = LegendaryPokemonDAO()
        self.shiny_pkmn = ShinyPokemonRatesDAO()
        self.trainer_data = TrainerDAO()
        self.ultra_beasts = UltraBeastsDAO()
        