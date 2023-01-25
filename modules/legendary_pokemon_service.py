from database import LegendaryPokemonDAO


class LegendaryPokemonService:
    def __init__(self) -> None:
        self.legendary_dao = LegendaryPokemonDAO()

    def is_pokemon_legendary(self, pkmn_name: str) -> bool:
        """
        Gives the pokemon to the trainer in their inventory
        """
        if pkmn_name in self.legendary_dao.get_legendary_pokemon():
            return True
        return False
