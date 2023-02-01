from classes import DataDAO


GIFT_JSON_NAME = "gift.json"


class GiftDAO(DataDAO):
    """
    Gets the available gifts to receive
    from PokeBot as well as the gift
    availability state
    """
    def __init__(self, filename=GIFT_JSON_NAME):
        if (self.__initialized):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GiftDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_gift_list_pokemon(self) -> dict:
        """
        Gets the list of gifted pokemon to receive from
        PokeBot
        """
        return self.data["gift_list"]["pokemon"]

    def get_gift_list_lootbox(self) -> dict:
        """
        Gets the list of gifted lootboxes to receive from
        PokeBot
        """
        return self.data["gift_list"]["lootbox"]

    def get_gift_availability(self) -> bool:
        """
        Gets the state of whether trainers can
        receive a gift or not
        """
        return self.data["is_gift_available"]
