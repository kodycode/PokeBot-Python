from classes import ConfigDAO


LOOTBOX_CONFIG_NAME = "lootbox_rates_config.json"


class LootboxConfigsDAO(ConfigDAO):
    """
    Gets the configs for lootboxes
    """
    def __init__(self, filename=LOOTBOX_CONFIG_NAME):
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LootboxConfigsDAO, cls).__new__(cls)
            return cls.instance
        return cls.instance

    def get_lootbox_pokemon_limit(self) -> int:
        """
        Gets the number of pokemon that a lootbox
        opening can provide to the trainer
        """
        return self.data["lootbox_pokemon_limit"]

    def get_daily_lootbox_bronze_rate(self) -> float:
        """
        Gets the max number threshold for a bronze
        lootbox given by the daily token redemption
        """
        return self.data["daily_lootbox_bronze_rate"]

    def get_daily_lootbox_silver_rate(self) -> float:
        """
        Gets the max number threshold for a silver
        lootbox given by the daily token redemption
        """
        return self.data["daily_lootbox_silver_rate"]

    def get_daily_lootbox_gold_rate(self) -> float:
        """
        Gets the max number threshold for a gold
        lootbox given by the daily token redemption
        """
        return self.data["daily_lootbox_gold_rate"]

    def get_daily_lootbox_legendary_rate(self) -> float:
        """
        Gets the max number threshold for a legendary
        lootbox given by the daily token redemption
        """
        return self.data["daily_lootbox_legendary_rate"]

    def get_bronze_lootbox_daily_token_price(self) -> int:
        """
        Gets the daily token shop price to redeem a
        bronze lootbox
        """
        return self.data["bronze_lootbox_daily_token_price"]

    def get_silver_lootbox_daily_token_price(self) -> int:
        """
        Gets the daily token shop price to redeem a
        silver lootbox
        """
        return self.data["silver_lootbox_daily_token_price"]

    def get_gold_lootbox_daily_token_price(self) -> int:
        """
        Gets the daily token shop price to redeem a
        gold lootbox
        """
        return self.data["gold_lootbox_daily_token_price"]

    def get_lootbox_bronze_rate(self) -> float:
        """
        Gets the max number threshold for a bronze
        lootbox given given by catching a pokemon
        """
        return self.data["lootbox_bronze_rate"]

    def get_lootbox_silver_rate(self) -> float:
        """
        Gets the max number threshold for a silver
        lootbox given given by catching a pokemon
        """
        return self.data["lootbox_silver_rate"]

    def get_lootbox_gold_rate(self) -> float:
        """
        Gets the max number threshold for a gold
        lootbox given given by catching a pokemon
        """
        return self.data["lootbox_gold_rate"]

    def get_lootbox_legendary_rate(self) -> float:
        """
        Gets the max number threshold for a legendary
        lootbox given given by catching a pokemon
        """
        return self.data["lootbox_legendary_rate"]
