from classes import DataDAO


GIFT_JSON_NAME = "gift.json"

class GiftDAO(DataDAO):
    """
    Gets the available gifts to receive
    from PokeBot as well as the gift
    availability state
    """
    def __init__(self, filename=GIFT_JSON_NAME):
        super().__init__(filename)

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
