from discord.ext import commands
from modules import PokeBotCog


class MiscCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()

    # @commands.command(name='gif', pass_context=True)
    # async def gif(self, ctx, pkmn_name: str, shiny=None):
    #     """
    #     Display a gif of the pokemon

    #     @param pkmn_name - name of the pokemon to find a gif of
    #     @param shiny - specify if pkmn is shiny or not
    #     """
    #     await self.cmd_function.display_gif(ctx, pkmn_name, shiny)

    # @commands.command(name='profile', pass_context=True)
    # async def profile(self, ctx, trainer):
    #     """
    #     Obtains the profile of a trainer specified

    #     @param trainer - trainer profile to search for
    #     """
    #     await self.cmd_function.display_trainer_profile(ctx, trainer)

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
