from classes import ConfigDAO


DAILY_CONFIG_NAME = "daily_shop_config.json"


class DailyShopDAO(ConfigDAO):
    """
    Gets the list of events that are available
    """
    def __init__(self, filename=DAILY_CONFIG_NAME):
        if (self.__initialized):
            return
        self.__initialized = True
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DailyShopDAO, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def get_daily_redemption_reset_hour(self) -> int:
        """
        Gets the daily redemption reset hour
        """
        return self.data["daily_redemption_reset_hour"]

    def get_daily_shop_menu(self) -> dict:
        """
        Gets the shop menu of the daily shop
        """
        return self.data["daily_shop_menu"]
