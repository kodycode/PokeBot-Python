from classes import DataDAO


ULTRA_BEASTS_FILE = "ultra_beasts.json"


class UltraBeastsDAO(DataDAO):
    """
    Accesses the list of known ultra beasts
    """
    def __init__(self, filename=ULTRA_BEASTS_FILE):
        if (self.__initialized):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UltraBeastsDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_ultra_beasts(self) -> list:
        """
        Gets the list of ultra beasts
        """
        return self.data
