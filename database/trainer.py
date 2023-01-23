from classes import DataDAO


TRAINER_JSON_FILE = "trainers.json"


class TrainerDAO(DataDAO):
    """
    Accesses, modifies and returns the PokeBot JSON data
    """
    PINVENTORY = "pinventory"
    LAST_CATCH_TIME = "last_catch_time"
    LAST_DAILY_REDEEMED_TIME = "last_daily_redeemed_time"
    LOOTBOX = "lootbox"
    DAILY_TOKENS = "daily_tokens"

    def __init__(self, user_id: str, filename=TRAINER_JSON_FILE):
        super().__init__(filename)
        self.user_id = user_id
        self.trainer_data = self.data[self.user_id]

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TrainerDAO, cls).__new__(cls)
            return cls.instance

    def get_pokemon_inventory(self) -> dict:
        """
        Gets the inventory of pokemon from the trainer
        """
        return self.trainer_data[self.PINVENTORY]

    def get_last_catch_time(self) -> float:
        """
        Gets the last catch time of the trainer
        """
        return self.trainer_data[self.LAST_CATCH_TIME]

    def get_last_daily_redeemed_time(self) -> float:
        """
        Gets the last daily redeemed time of the trainer
        """
        return self.trainer_data[self.LAST_DAILY_REDEEMED_TIME]

    def get_lootbox_inventory(self) -> dict:
        """
        Gets the inventory of lootboxes that the trainer has
        """
        return self.trainer_data[self.LOOTBOX]

    def get_daily_tokens(self) -> int:
        """
        Gets the list of daily tokens that the trainer has
        """
        return self.trainer_data[self.DAILY_TOKENS]

    def set_pokemon_inventory(self, pkmn_name: str, quantity: int) -> None:
        """
        Sets the quantity of a specific trainer's pokemon
        within their inventory
        """
        self.data[self.user_id][self.PINVENTORY][pkmn_name] = quantity

    def set_last_catch_time(self, time: float) -> None:
        """
        Sets the trainer's last daily redeemed time
        """
        self.data[self.user_id][self.LAST_CATCH_TIME] = time

    def set_last_daily_redeemed_time(self, time: float) -> None:
        """
        Sets the trainer's last daily redeemed time
        """
        self.data[self.user_id][self.LAST_DAILY_REDEEMED_TIME] = time

    def set_lootbox_inventory(self, lootbox_tier_name: str, quantity: int) -> None:
        """
        Sets the quantity of a specific lootbox tier within
        the trainer's inventory
        """
        self.data[self.user_id][self.LOOTBOX][lootbox_tier_name] = quantity

    def set_daily_tokens(self, quantity: int) -> None:
        """
        Sets the trainer's daily token amount
        """
        self.data[self.user_id][self.DAILY_TOKENS] = quantity
