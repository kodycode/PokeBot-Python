from classes import PokeBotModule
from modules.pokebot_rates import PokeBotRates
from modules.trainer_service import TrainerService
import discord


class MiscLogicException(Exception):
    pass


class MiscLogic(PokeBotModule):
    """Handles the misc logic of features for PokeBot"""

    def __init__(self, bot):
        self.trainer_service = TrainerService(bot, PokeBotRates(bot))

    async def display_trainer_profile(
        self,
        ctx: discord.ext.commands.Command,
        user_mention: str
    ):
        """
        Displays trainer profile and pokemon caught stats
        """
        await self.trainer_service.display_trainer_profile(ctx, user_mention)
