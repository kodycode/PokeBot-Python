# from modules.pokemon_functionality import PokemonFunctionality
from classes import PokeBotCog
from discord.ext import commands


class AdminCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()

    # @commands.command(name='give', pass_context=True, hidden=True)
    # @commands.check(check_if_it_is_me)
    # async def give(self, ctx, user_id, pkmn_name, shiny=None):
    #     """
    #     Gives a pokemon to a trainer (admin only cmd)

    #     @param ctx - context of the command sent
    #     @param user_id - user to give pokemon to
    #     @param pkmn_name - name of the pokemon to give to user
    #     @param shiny - 's' or 'shiny' if shiny
    #     """
    #     await self.cmd_function.give_trainer_pokemon(ctx,
    #                                                  user_id,
    #                                                  pkmn_name,
    #                                                  shiny)

    # @commands.command(name='delete', pass_context=True, hidden=True)
    # async def delete(self, ctx, user_id, pkmn_name, shiny=False):
    #     """
    #     Deletes a pokemon from the trainer (admin only cmd)

    #     @param ctx - context of the command sent
    #     @param user_id - user to give pokemon to
    #     @param pkmn_name - name of the pokemon to delete from the user
    #     @param shiny - 's' or 'shiny' if shiny
    #     """
    #     await self.cmd_function.delete_trainer_pokemon(ctx,
    #                                                    user_id,
    #                                                    pkmn_name,
    #                                                    shiny)

    # @commands.command(name='giveloot', pass_context=True, hidden=True)
    # async def giveloot(self, ctx, user_id, lootbox):
    #     """
    #     Gives a trainer a specified lootbox

    #     @param ctx - context of the command sent
    #     @param user_id - user to give pokemon to
    #     @param lootbox - lootbox to give to the user
    #     """
    #     await self.cmd_function.give_trainer_lootbox(ctx,
    #                                                  user_id,
    #                                                  lootbox)

    # @commands.command(name='deleteloot', pass_context=True, hidden=True)
    # async def deleteloot(self, ctx, user_id, lootbox):
    #     """
    #     Deletes a lootbox from a trainer's inventory

    #     @param ctx - context of the command sent
    #     @param user_id - user to give pokemon to
    #     @param lootbox - lootbox to remove
    #     """
    #     await self.cmd_function.delete_trainer_lootbox(ctx,
    #                                                    user_id,
    #                                                    lootbox)
