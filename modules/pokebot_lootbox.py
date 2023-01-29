from classes import PokeBotModule
from modules.pokebot_rates import PokeBotRates
from modules.pokebot_exceptions import PokeBotLootboxException
import random


class PokeBotLootbox(PokeBotModule):

    def __init__(self, rates: PokeBotRates):
        self.rates = rates

    def generate_lootbox(self, daily=False) -> str:
        """
        Generates a lootbox with consideration into daily or catch rates
        """
        try:
            lootbox_rng = random.uniform(0, 1)
            if daily:
                lootbox_bronze_rate = \
                    self.rates.get_daily_lootbox_bronze_rate()
                lootbox_silver_rate = \
                    self.rates.get_daily_lootbox_silver_rate()
                lootbox_gold_rate = \
                    self.rates.get_daily_lootbox_gold_rate()
            else:
                lootbox_bronze_rate = \
                    self.rates.get_lootbox_bronze_rate()
                lootbox_silver_rate = \
                    self.rates.get_lootbox_silver_rate()
                lootbox_gold_rate = \
                    self.rates.get_lootbox_gold_rate()
            if lootbox_rng < lootbox_gold_rate:
                return "gold"
            elif lootbox_rng < lootbox_silver_rate:
                return "silver"
            elif lootbox_rng < lootbox_bronze_rate:
                return "bronze"
            return None
        except Exception as e:
            msg = "Error has occurred in generating lootbox."
            self.post_error_log_msg(PokeBotLootboxException.__name__, msg, e)
            raise

