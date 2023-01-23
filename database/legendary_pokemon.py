from classes import DataDAO


LEGENDARY_JSON_NAME = "legendary_pkmn.json"


class LegendaryPokemonDAO(DataDAO):
    """
    Accesses the list of known legendary pokemon
    """
    def __init__(self, filename=LEGENDARY_JSON_NAME):
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LegendaryPokemonDAO, cls).__new__(cls)
            return cls.instance
        return cls.instance

    def get_legendary_pokemon(self) -> list:
        """
        Gets the list of legendary pokemon
        """
        return self.data
