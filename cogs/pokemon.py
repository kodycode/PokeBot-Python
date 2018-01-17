from cogs.modules.pokemon_functionality import PokemonFunctionality
from discord.ext import commands


class PokemonCommands:
    """Handles Pokemon related commands"""

    def __init__(self, bot):
        self.cmd_function = PokemonFunctionality(bot)

    @commands.command(name='reload', hidden=True)
    async def reload(self):
        """
        Reloads pokemon data
        """
        await self.cmd_function.reload_data()

    @commands.command(name='pokemon', pass_context=True)
    async def pokemon(self, ctx):
        """
        Catches a random pokemon

        @param ctx - context of the command sent
        """
        await self.cmd_function.catch_pokemon(ctx)

    @commands.command(name='inventory', pass_context=True)
    async def pinventory(self, ctx, page_number=0):
        """
        Displays the trainer's pokemon inventory

        @param ctx - context of the command sent
        """
        await self.cmd_function.display_pinventory(ctx, page_number)

    @commands.command(name='gif')
    async def gif(self, pkmn_name: str, shiny=None):
        """
        Display a gif of the pokemon

        @param pkmn_name - name of the pokemon to find a gif of
        @param shiny - specify if pkmn is shiny or not
        """
        await self.cmd_function.display_gif(pkmn_name, shiny)

    @commands.command(name='profile')
    async def profile(self, trainer):
        """
        Obtains the profile of a trainer specified
        """
        await self.cmd_function.display_trainer_profile(trainer)

    @commands.command(name='ranking')
    async def ranking(self, option="t"):
        """
        Displays ranking of all the trainers
        """
        await self.cmd_function.display_ranking(option)
