from bot_logger import logger
from classes import PokeBotCog
from discord import Embed
from discord.ext import commands
from modules import MiscLogic


class MiscCommandsException(Exception):
    pass


class MiscCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()
        self.pokebot_misc_logic = MiscLogic(bot)


    @commands.command(name='gif', pass_context=True)
    async def gif(self, ctx, pkmn_name: str, shiny: str=None):
        """
        Display a gif of the pokemon
        """
        try:
            em = Embed()
            if shiny == "shiny" or shiny == "s":
                em.set_image(url="https://play.pokemonshowdown.com/sprites/"
                                 "xyani-shiny/{}.gif"
                                 "".format(pkmn_name))
            else:
                em.set_image(url="https://play.pokemonshowdown.com/sprites/"
                                 "xyani/{}.gif"
                                 "".format(pkmn_name))
            await ctx.send(embed=em)
        except MiscCommandsException as e:
            print("An error has occurred in displaying a gif. "
                  "See error.log.")
            logger.error("MiscCommandsException: {}".format(str(e)))

    @commands.command(name='profile', pass_context=True)
    async def profile(
        self, 
        ctx: commands.Context, 
        user_mention: str=commands.parameter(description="The @-mention of the user on disord.")
    ):
        """
        Obtains the profile of a trainer specified
        """
        await self.pokebot_misc_logic.display_trainer_profile(ctx, user_mention)

    # @commands.command(name='ranking', pass_context=True)
    # async def ranking(self, ctx, option="t"):
    #     """
    #     Displays ranking of all the trainers

    #     @param option - options are:
    #                     l - legendary
    #                     s - shiny
    #                     t - total (default)
    #                     u - ultra
    #     """
    #     await self.cmd_function.display_ranking(ctx, option)
