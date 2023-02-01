from classes import ConfigDAO


SHINY_CONFIG_NAME = "shiny_pkmn_rate_config.json"


class ShinyPokemonRatesDAO(ConfigDAO):
    """
    Retrieves the shiny pokemon rates
    """
    def __init__(self, filename=SHINY_CONFIG_NAME):
        if (self.__initialized):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ShinyPokemonRatesDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_shiny_pkmn_catch_rate(self) -> float:
        """
        Gets the shiny pokemon catch rate
        """
        return self.data["shiny_pkmn_catch_rate"]

    def get_shiny_pkmn_hatch_multiplier(self) -> int:
        """
        Gets the shiny multiplier of hatching pokemon
        """
        return self.data["shiny_hatch_multiplier"]

    def get_shiny_pkmn_exchange_multiplier(self) -> int:
        """
        Gets the shiny multiplier of exchanging pokemon
        """
        return self.data["shiny_exchange_multiplier"]

    def get_shiny_pkmn_lootbox_multiplier(self) -> int:
        """
        Gets the shiny multiplier of getting pokemon
        via lootboxes
        """
        return self.data["shiny_lootbox_multiplier"]
