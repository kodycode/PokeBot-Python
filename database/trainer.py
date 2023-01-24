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

    def __init__(self, filename=TRAINER_JSON_FILE):
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TrainerDAO, cls).__new__(cls)
            return cls.instance
        return cls.instance

    def is_existing_trainer(self, user_id: str) -> bool:
        """
        Checks if trainer exists and returns True if so,
        otherwise False
        """
        return bool(self.data.get(user_id, False))

    def get_pokemon_inventory(self, user_id: str) -> dict:
        """
        Gets the inventory of pokemon from the trainer
        """
        return self.data[user_id][self.PINVENTORY]

    def get_last_catch_time(self, user_id: str) -> float:
        """
        Gets the last catch time of the trainer
        """
        return self.data[user_id][self.LAST_CATCH_TIME]

    def get_last_daily_redeemed_time(self, user_id: str) -> float:
        """
        Gets the last daily redeemed time of the trainer
        """
        return self.data[user_id][self.LAST_DAILY_REDEEMED_TIME]

    def get_lootbox_inventory(self, user_id: str) -> dict:
        """
        Gets the inventory of lootboxes that the trainer has
        """
        return self.data[user_id][self.LOOTBOX]

    def get_daily_tokens(self, user_id: str) -> int:
        """
        Gets the list of daily tokens that the trainer has
        """
        return self.data[user_id][self.DAILY_TOKENS]

    def set_pokemon_inventory(self, user_id: str, pkmn_name: str, quantity: int) -> None:
        """
        Sets the quantity of a specific trainer's pokemon
        within their inventory
        """
        self.data[user_id][self.PINVENTORY][pkmn_name] = quantity

    def set_last_catch_time(self, user_id: str, time: float) -> None:
        """
        Sets the trainer's last daily redeemed time
        """
        self.data[user_id][self.LAST_CATCH_TIME] = time

    def set_last_daily_redeemed_time(self, user_id: str, time: float) -> None:
        """
        Sets the trainer's last daily redeemed time
        """
        self.data[user_id][self.LAST_DAILY_REDEEMED_TIME] = time

    def set_lootbox_inventory(self, user_id: str, lootbox_tier_name: str, quantity: int) -> None:
        """
        Sets the quantity of a specific lootbox tier within
        the trainer's inventory
        """
        self.data[user_id][self.LOOTBOX][lootbox_tier_name] = quantity

    def set_daily_tokens(self, user_id: str, quantity: int) -> None:
        """
        Sets the trainer's daily token amount
        """
        self.data[user_id][self.DAILY_TOKENS] = quantity

    def generate_new_trainer(self, user_id: str) -> None:
        """
        Generates a new trainer in the database
        """
        self.data[user_id] = {}
        self.data[user_id][self.PINVENTORY] = {}
        self.data[user_id][self.LOOTBOX] = {
            "bronze": 0,
            "silver": 0,
            "gold": 0,
            "legendary": 0,
        }
        self.data[user_id][self.LAST_CATCH_TIME] = 0
        self.data[user_id][self.LAST_DAILY_REDEEMED_TIME] = 0
        self.data[user_id][self.DAILY_TOKENS] = 0
