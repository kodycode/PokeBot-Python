from bot_logger import logger
from classes import PokeBotModule
from modules.pokebot_exceptions import (
    MiscLogicException,
    UnregisteredTrainerException
)
from modules.pokebot_rates import PokeBotRates
from modules.services.trainer_service import TrainerService
from utils import parse_discord_mention_user_id, get_ctx_user_id
import discord


class MiscLogic(PokeBotModule):
    """Handles the misc logic of features for PokeBot"""

    def __init__(self, bot):
        self.trainer_service = TrainerService(PokeBotRates(bot))

    async def build_gif_embed(
        self,
        pkmn_name: str,
        shiny: str
    ) -> discord.Embed:
        """
        Builds the gif message to display
        """
        try:
            em = discord.Embed()
            if shiny == "shiny" or shiny == "s":
                em.set_image(url="https://play.pokemonshowdown.com/sprites/"
                                 "xyani-shiny/{}.gif"
                                 "".format(pkmn_name))
            else:
                em.set_image(url="https://play.pokemonshowdown.com/sprites/"
                                 "xyani/{}.gif"
                                 "".format(pkmn_name))
            return em
        except MiscLogicException as e:
            print("An error has occurred in displaying a gif. "
                  "See error.log.")
            logger.error("MiscCommandsException: {}".format(str(e)))

    async def build_trainer_profile_msg(
        self,
        ctx: discord.ext.commands.Command,
        user_mention: str
    ) -> discord.Embed:
        """
        Displays trainer profile and pokemon caught stats
        """
        try:
            # Discords 'get_user' API uses int user_id
            # Whereas our JSON file keeps it as str
            user_id = parse_discord_mention_user_id(user_mention)
            user_obj = ctx.bot.get_user(int(user_id))
            return await self.trainer_service.display_trainer_profile(user_obj)
        except UnregisteredTrainerException:
            raise
