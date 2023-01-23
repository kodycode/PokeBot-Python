from database import GeneralRatesDAO, LootboxConfigsDAO, ShinyPokemonRatesDAO
from events import EventManager


class PokeBotRates:
    """Holds the values of the PokeBot rates to use and
    opens options here for event modification to the
    rates (i.e. Happy Hour shiny rate/cooldown)"""

    def __init__(self):
        self.event_manager = EventManager()
        self.general_rates = GeneralRatesDAO()
        self.lootbox_rates = LootboxConfigsDAO()
        self.shiny_pkmn_rates = ShinyPokemonRatesDAO()

    def get_daily_redemption_reset_hour(self) -> int:
        """
        Gets the hour to reset the daily applied with
        any event modifications
        """
        return self.general_rates.get_daily_redemption_reset_hour()

    def get_catch_cooldown_seconds(self) -> int:
        """
        Gets the catch cooldown applied with any event
        modifications
        """
        return self.general_rates.get_catch_cooldown_seconds() \
            * self.event_manager.get_event_catch_cooldown_modifier()

    def get_shiny_pkmn_catch_rate(self) -> int:
        """
        Gets the shiny pokemon catch rate
        applied with any event modifications
        """
        return self.shiny_pkmn_rates.get_shiny_pkmn_catch_rate() \
            * self.event_manager.get_event_shiny_catch_rate_modifier()

    def get_shiny_pkmn_hatch_multiplier(self) -> int:
        """
        Gets the shiny multiplier of hatching pokemon
        applied with any event modifications
        """
        return self.shiny_pkmn_rates.get_shiny_pkmn_hatch_multiplier()

    def get_shiny_pkmn_exchange_multiplier(self) -> int:
        """
        Gets the shiny multiplier of exchanging pokemon
        applied with any event modifications
        """
        return self.shiny_pkmn_rates.get_shiny_pkmn_exchange_multiplier()

    def get_shiny_pkmn_lootbox_multiplier(self) -> int:
        """
        Gets the shiny multiplier of getting pokemon
        via lootboxes applied with any event modifications
        """
        return self.shiny_pkmn_rates.get_shiny_pkmn_lootbox_multiplier()

    def get_random_shiny_daily_token_price(self) -> int:
        """
        Gets the daily token shop price to redeem a
        random shiny pokemon applied with any event modifications
        """
        return self.shiny_pkmn_rates.get_random_shiny_daily_token_price()

    def get_lootbox_pokemon_limit(self) -> int:
        """
        Gets the number of pokemon that a lootbox
        opening can provide to the trainer
        """
        return self.lootbox_rates.get_lootbox_pokemon_limit()
    
    def get_daily_lootbox_bronze_rate(self) -> float:
        """
        Gets the max number threshold for a bronze
        lootbox given by the daily token redemption
        """
        return self.lootbox_rates.get_daily_lootbox_bronze_rate()

    def get_daily_lootbox_silver_rate(self) -> float:
        """
        Gets the max number threshold for a silver
        lootbox given by the daily token redemption
        """
        return self.lootbox_rates.get_daily_lootbox_silver_rate()

    def get_daily_lootbox_gold_rate(self) -> float:
        """
        Gets the max number threshold for a gold
        lootbox given by the daily token redemption
        """
        return self.lootbox_rates.get_daily_lootbox_gold_rate()

    def get_daily_lootbox_legendary_rate(self) -> float:
        """
        Gets the max number threshold for a legendary
        lootbox given by the daily token redemption
        """
        return self.lootbox_rates.get_daily_lootbox_legendary_rate()

    def get_bronze_lootbox_daily_token_price(self) -> int:
        """
        Gets the daily token shop price to redeem a
        bronze lootbox
        """
        return self.lootbox_rates.get_bronze_lootbox_daily_token_price()

    def get_silver_lootbox_daily_token_price(self) -> int:
        """
        Gets the daily token shop price to redeem a
        silver lootbox
        """
        return self.lootbox_rates.get_silver_lootbox_daily_token_price()

    def get_gold_lootbox_daily_token_price(self) -> int:
        """
        Gets the daily token shop price to redeem a
        gold lootbox
        """
        return self.lootbox_rates.get_gold_lootbox_daily_token_price()

    def get_legendary_lootbox_daily_token_price(self) -> int:
        """
        Gets the daily token shop price to redeem a
        legendary lootbox
        """
        return self.lootbox_rates.get_legendary_lootbox_daily_token_price()

    def get_lootbox_bronze_rate(self) -> float:
        """
        Gets the max number threshold for a bronze
        lootbox given given by catching a pokemon
        """
        return self.lootbox_rates.get_lootbox_bronze_rate()

    def get_lootbox_silver_rate(self) -> float:
        """
        Gets the max number threshold for a silver
        lootbox given given by catching a pokemon
        """
        return self.lootbox_rates.get_lootbox_silver_rate()

    def get_lootbox_gold_rate(self) -> float:
        """
        Gets the max number threshold for a gold
        lootbox given given by catching a pokemon
        """
        return self.lootbox_rates.get_lootbox_gold_rate()

    def get_lootbox_legendary_rate(self) -> float:
        """
        Gets the max number threshold for a legendary
        lootbox given given by catching a pokemon
        """
        return self.lootbox_rates.get_lootbox_legendary_rate()
