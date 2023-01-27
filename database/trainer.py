from classes import DataDAO


TRAINER_JSON_FILE = "trainers.json"


class TrainerDAO(DataDAO):
    """
    Accesses, modifies and returns the PokeBot JSON data
    """
    EGG_COUNT = "egg_count"
    EGG_MANAPHY_COUNT = "egg_manaphy_count"
    PINVENTORY = "pinventory"
    LAST_CATCH_TIME = "last_catch_time"
    LAST_DAILY_REDEEMED_TIME = "last_daily_redeemed_time"
    LOOTBOX = "lootbox"
    DAILY_TOKENS = "daily_tokens"
    LEGENDARY_PKMN_COUNT = "legendary_pkmn_count"
    SHINY_PKMN_COUNT = "shiny_pkmn_count"
    TOTAL_PKMN_COUNT = "total_pkmn_count"
    ULTRA_BEASTS_COUNT = "ultra_beasts_count"

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

    def get_pokemon_quantity(self, user_id: str, pkmn_name: str) -> int:
        """
        Gets the number of a specific pokemon from the inventory
        """
        if pkmn_name not in self.data[user_id][self.PINVENTORY]:
            return 0
        return self.data[user_id][self.PINVENTORY][pkmn_name]

    def increment_pokemon_quantity(self, user_id: str, pkmn_name: str) -> None:
        """
        Increments the quantity of a specific trainer's pokemon
        within their inventory
        """
        pinventory = self.get_pokemon_inventory(user_id)
        if pkmn_name not in pinventory:
            self.set_pokemon_quantity(user_id, pkmn_name, 1)
        else:
            self.data[user_id][self.PINVENTORY][pkmn_name] += 1

    def set_pokemon_quantity(self, user_id: str, pkmn_name: str, quantity: int) -> None:
        """
        Sets the quantity of a specific trainer's pokemon
        within their inventory
        """
        if quantity <= 0:
            del self.data[user_id][self.PINVENTORY][pkmn_name]
        else:
            self.data[user_id][self.PINVENTORY][pkmn_name] = quantity

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

    def increment_lootbox_quantity(self, user_id: str, lootbox) -> None:
        """
        Increments the quantity of the lootbox specified in the trainer's
        inventory
        """
        self.data[user_id][self.LOOTBOX][lootbox] += 1

    def get_daily_tokens(self, user_id: str) -> int:
        """
        Gets the list of daily tokens that the trainer has
        """
        return self.data[user_id][self.DAILY_TOKENS]

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
        self.data[user_id][self.LEGENDARY_PKMN_COUNT] = 0
        self.data[user_id][self.SHINY_PKMN_COUNT] = 0
        self.data[user_id][self.TOTAL_PKMN_COUNT] = 0
        self.data[user_id][self.ULTRA_BEASTS_COUNT] = 0

    def get_total_pokemon_caught(self) -> int:
        """
        Gets the total amount of pokemon caught across
        all trainers

        TODO: Load and save to DB total pokemon count?
        """
        total_pokemon_caught = 0
        for trainer in self.data:
            pinventory = self.data[trainer][self.PINVENTORY]
            for pkmn in pinventory:
                total_pokemon_caught += pinventory[pkmn]
        return total_pokemon_caught

    def get_legendary_pkmn_count(self, user_id: str) -> int:
        """
        Gets the legendary pokemon count
        """
        return self.data[user_id][self.LEGENDARY_PKMN_COUNT]

    def increment_legendary_pkmn_count(self, user_id: str) -> None:
        """
        Increments the trainer's count for legendary pokemon
        """
        self.data[user_id][self.LEGENDARY_PKMN_COUNT] += 1

    def get_shiny_pkmn_count(self, user_id: str) -> int:
        """
        Gets the shiny pokemon count
        """
        return self.data[user_id][self.SHINY_PKMN_COUNT]

    def increment_shiny_pkmn_count(self, user_id: str) -> None:
        """
        Increments the trainer's count for shiny pokemon
        """
        self.data[user_id][self.SHINY_PKMN_COUNT] += 1

    def get_total_pkmn_count(self, user_id: str) -> int:
        """
        Gets the total pokemon count
        """
        return self.data[user_id][self.TOTAL_PKMN_COUNT]

    def increment_total_pkmn_count(self, user_id: str) -> None:
        """
        Increments the trainer's count for total pokemon
        """
        self.data[user_id][self.TOTAL_PKMN_COUNT] += 1

    def get_ultra_beasts_count(self, user_id: str) -> int:
        """
        Gets the ultra beasts count
        """
        return self.data[user_id][self.ULTRA_BEASTS_COUNT]

    def increment_ultra_beasts_count(self, user_id: str) -> None:
        """
        Increments the trainer's count for legendary pokemon
        """
        self.data[user_id][self.ULTRA_BEASTS_COUNT] += 1

    def get_egg_count(self, user_id: str) -> int:
        """
        Gets the amount of eggs that exist with the user
        """
        return self.data[user_id][self.EGG_COUNT]

    def get_egg_manaphy_count(self, user_id: str) -> int:
        """
        Gets the amount of manaphy eggs that exist with the user
        """
        return self.data[user_id][self.EGG_MANAPHY_COUNT]

    def decrement_egg_count(self, user_id: str) -> None:
        """
        Decrement trainer's egg count
        """
        self.data[user_id][self.EGG_COUNT] -= 1

    def decrement_egg_manaphy_count(self, user_id: str) -> None:
        """
        Decrement trainer's manaphy egg count
        """
        self.data[user_id][self.EGG_MANAPHY_COUNT] -= 1
