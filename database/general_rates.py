from classes import ConfigDAO


GENERAL_CONFIG_NAME = "general_config.json"


class GeneralRatesDAO(ConfigDAO):
    """
    Gets the general rate configs for PokeBot
    """
    def __init__(self, filename=GENERAL_CONFIG_NAME):
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GeneralRatesDAO, cls).__new__(cls)
            return cls.instance
        return cls.instance

    def get_daily_redemption_reset_hour(self) -> int:
        """
        Gets the hour to reset the daily
        """
        return self.data["daily_redemption_reset_hour"]

    def get_catch_cooldown_seconds(self) -> int:
        """
        Gets the list of gifted lootboxes to receive from
        PokeBot
        """
        return self.data["catch_cooldown_seconds"]
