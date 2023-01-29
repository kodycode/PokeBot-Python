from modules.pokebot_exceptions import PokeBotStatusException
from modules.pokebot_rates import PokeBotRates
from modules.services import TrainerService
import discord


class PokeBotStatus:
    def __init__(self, bot):
        if(self.__initialized): return
        self.__initialized = True
        self.bot = bot
        self.rates = PokeBotRates(bot)
        self.trainer_service = TrainerService(self.rates)
        self.total_pkmn_count = \
            self.trainer_service.get_all_total_pokemon_caught_count()

    def __new__(*args):
        cls = args[0]
        if not hasattr(cls, 'instance'):
            cls.instance = super(PokeBotStatus, cls).__new__(cls)
            cls.__initialized = False
            return cls.instance
        return cls.instance

    def increase_total_pkmn_count(self, quantity: int):
        """
        Increments the total pokemon count
        """
        try:
            self.total_pkmn_count += 1
        except Exception as e:
            msg = "Failed to increment total pokemon count."
            self.post_error_log_msg(PokeBotStatusException.__name__, msg, e)
            raise

    def decrease_total_pkmn_count(self, quantity: int):
        """
        Decrements the total pokemon count
        """
        try:
            self.total_pkmn_count -= 1
        except Exception as e:
            msg = "Failed to increment total pokemon count."
            self.post_error_log_msg(PokeBotStatusException.__name__, msg, e)
            raise

    async def display_total_pokemon_caught(self) -> None:
        """
        Updates the bot status display with a pokemon count given
        """
        try:
            game_status = discord.Game(name=f"{self.total_pkmn_count}" \
                                             " Pokémon caught")
            await self.bot.change_presence(activity=game_status)
        except Exception as e:
            msg = "Failed to display total pokemon caught."
            self.post_error_log_msg(PokeBotStatusException.__name__, msg, e)
            raise
