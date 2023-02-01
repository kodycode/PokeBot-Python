from classes import PokeBotModule
from database import DailyShopDAO, GeneralRatesDAO, LootboxConfigsDAO, ShinyPokemonRatesDAO
from events import EventManager
from modules.pokebot_exceptions import PokeBotRatesException


class PokeBotRates(PokeBotModule):
    """Holds the values of the PokeBot rates to use and
    opens options here for event modification to the
    rates (i.e. Happy Hour shiny rate/cooldown)"""

    def __init__(self, bot):
        self.event_manager = EventManager(bot)
        self.daily_shop_rates = DailyShopDAO()
        self.general_rates = GeneralRatesDAO()
        self.lootbox_rates = LootboxConfigsDAO()
        self.shiny_pkmn_rates = ShinyPokemonRatesDAO()

    def get_daily_redemption_reset_hour(self) -> int:
        """
        Gets the hour to reset the daily applied with
        any event modifications
        """
        try:
            return self.daily_shop_rates.get_daily_redemption_reset_hour()
        except Exception as e:
            msg = "Error has occurred getting daily redemption hour."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_daily_shop_menu(self) -> dict:
        """
        Gets the daily shop menu
        """
        try:
            return self.daily_shop_rates.get_daily_shop_menu()
        except Exception as e:
            msg = "Error has occurred getting daily shop menu."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_catch_cooldown_seconds(self) -> int:
        """
        Gets the catch cooldown applied with any event
        modifications
        """
        try:
            return self.general_rates.get_catch_cooldown_seconds() \
                * self.event_manager.get_current_event_catch_cooldown_modifier()
        except Exception as e:
            msg = "Error has occurred getting catch cooldown seconds."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_shiny_pkmn_catch_rate(self) -> int:
        """
        Gets the shiny pokemon catch rate
        applied with any event modifications
        """
        try:
            return self.shiny_pkmn_rates.get_shiny_pkmn_catch_rate() \
                * self.event_manager.get_current_event_shiny_rate_modifier()
        except Exception as e:
            msg = "Error has occurred getting shiny pkmn catch rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_shiny_pkmn_night_vendor_rate(self) -> int:
        """
        Gets the shiny pokemon spawn rate from a night vendor
        """
        try:
            nv_event = self.event_manager.get_event_by_key("night_vendor")
            return self.shiny_pkmn_rates.get_shiny_pkmn_catch_rate() \
                * nv_event.get_shiny_roll_rate_modifier()
        except Exception as e:
            msg = "Error has occurred getting shiny pkmn night vendor rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_shiny_pkmn_hatch_multiplier(self) -> int:
        """
        Gets the shiny multiplier of hatching pokemon
        applied with any event modifications
        """
        try:
            shiny_pkmn_hatch_multiplier = \
                self.shiny_pkmn_rates.get_shiny_pkmn_hatch_multiplier()
            shiny_pkmn_catch_rate = \
                self.shiny_pkmn_rates.get_shiny_pkmn_catch_rate()
            return shiny_pkmn_hatch_multiplier * shiny_pkmn_catch_rate
        except Exception as e:
            msg = "Error has occurred getting shiny pkmn hatch multiplier."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_shiny_pkmn_exchange_multiplier(self) -> int:
        """
        Gets the shiny multiplier of exchanging pokemon
        applied with any event modifications
        """
        try:
            return self.shiny_pkmn_rates.get_shiny_pkmn_exchange_multiplier()
        except Exception as e:
            msg = "Error has occurred getting shiny pkmn exchange multiplier."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_shiny_pkmn_lootbox_multiplier(self) -> int:
        """
        Gets the shiny multiplier of getting pokemon
        via lootboxes applied with any event modifications
        """
        try:
            return self.shiny_pkmn_rates.get_shiny_pkmn_lootbox_multiplier()
        except Exception as e:
            msg = "Error has occurred getting shiny pkmn lootbox multiplier."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_lootbox_pokemon_limit(self) -> int:
        """
        Gets the number of pokemon that a lootbox
        opening can provide to the trainer
        """
        try:
            return self.lootbox_rates.get_lootbox_pokemon_limit()
        except Exception as e:
            msg = "Error has occurred getting lootbox pokemon limit."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_daily_lootbox_bronze_rate(self) -> float:
        """
        Gets the max number threshold for a bronze
        lootbox given by the daily token redemption
        """
        try:
            return self.lootbox_rates.get_daily_lootbox_bronze_rate()
        except Exception as e:
            msg = "Error has occurred getting daily lootbox bronze rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_daily_lootbox_silver_rate(self) -> float:
        """
        Gets the max number threshold for a silver
        lootbox given by the daily token redemption
        """
        try:
            return self.lootbox_rates.get_daily_lootbox_silver_rate()
        except Exception as e:
            msg = "Error has occurred getting daily lootbox silver rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_daily_lootbox_gold_rate(self) -> float:
        """
        Gets the max number threshold for a gold
        lootbox given by the daily token redemption
        """
        try:
            return self.lootbox_rates.get_daily_lootbox_gold_rate()
        except Exception as e:
            msg = "Error has occurred getting daily lootbox gold rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_daily_lootbox_legendary_rate(self) -> float:
        """
        Gets the max number threshold for a legendary
        lootbox given by the daily token redemption
        """
        try:
            return self.lootbox_rates.get_daily_lootbox_legendary_rate()
        except Exception as e:
            msg = "Error has occurred getting daily lootbox legendary rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_lootbox_bronze_rate(self) -> float:
        """
        Gets the max number threshold for a bronze
        lootbox given given by catching a pokemon
        """
        try:
            return self.lootbox_rates.get_lootbox_bronze_rate()
        except Exception as e:
            msg = "Error has occurred getting lootbox bronze rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_lootbox_silver_rate(self) -> float:
        """
        Gets the max number threshold for a silver
        lootbox given given by catching a pokemon
        """
        try:
            return self.lootbox_rates.get_lootbox_silver_rate()
        except Exception as e:
            msg = "Error has occurred getting lootbox silver rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_lootbox_gold_rate(self) -> float:
        """
        Gets the max number threshold for a gold
        lootbox given given by catching a pokemon
        """
        try:
            return self.lootbox_rates.get_lootbox_gold_rate()
        except Exception as e:
            msg = "Error has occurred getting lootbox gold rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)

    def get_lootbox_legendary_rate(self) -> float:
        """
        Gets the max number threshold for a legendary
        lootbox given given by catching a pokemon
        """
        try:
            return self.lootbox_rates.get_lootbox_legendary_rate()
        except Exception as e:
            msg = "Error has occurred getting lootbox legendary rate."
            self.post_error_log_msg(PokeBotRatesException.__name__, msg, e)
