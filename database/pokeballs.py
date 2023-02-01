from classes import DataDAO
import random


POKEBALL_JSON_NAME = "pokeballs.json"


class PokeballsDAO(DataDAO):
    """
    Gets the list of all pokeball
    """
    def __init__(self, filename=POKEBALL_JSON_NAME):
        if (self.__initialized):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PokeballsDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_random_pokeball_emoji(self) -> str:
        """
        Gets a random pokeball from the list of pokeball emojis
        available
        """
        if not self.data:
            return ''
        return random.choice(list(self.data))
