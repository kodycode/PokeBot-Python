from database import UltraBeastsDAO


class UltraBeastsService:
    def __init__(self) -> None:
        self.ultra_beasts_dao = UltraBeastsDAO()

    def is_pokemon_ultra_beast(self, pkmn_name: str) -> bool:
        """
        Checks to see if the pokemon is an ultra beast
        """
        if pkmn_name in self.ultra_beasts_dao.get_ultra_beasts():
            return True
        return False
