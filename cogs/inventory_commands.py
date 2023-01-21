# from cogs.modules.pokemon_functionality import PokemonFunctionality
from discord.ext import commands
from modules import PokeBotCog


class InventoryCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()
        # self.cmd_function = PokemonFunctionality(bot)

    # @commands.command(name='catch', aliases=['c'], pass_context=True)
    # async def catch(self, ctx):
    #     """
    #     Catches a random pokemon

    #     @param ctx - context of the command sent
    #     """
    #     await self.cmd_function.catch_pokemon(ctx)

    # @commands.command(name='inventory', aliases=['i'], pass_context=True)
    # async def pinventory(self, ctx, page_number=0):
    #     """
    #     Displays the trainer's pokemon inventory

    #     @param ctx - context of the command sent
    #     @param page_number - page number in inventory
    #     """
    #     await self.cmd_function.display_pinventory(ctx, page_number)

    # @commands.command(name='release', aliases=['r'], pass_context=True)
    # async def release(self, ctx, pkmn: str, quantity=1):
    #     """
    #     Releases a pokemon from your inventory

    #     @param pkmn - pkmn to be released
    #     """
    #     await self.cmd_function.release_pokemon(ctx, pkmn, quantity)

    # @commands.command(name='hatch', aliases=['h'], pass_context=True)
    # async def hatch(self, ctx):
    #     """
    #     Hatches an egg from your inventory

    #     @param pkmn - pkmn to be released
    #     """
    #     await self.cmd_function.hatch_egg(ctx)

    # @commands.command(name='fuse', aliases=['f'], pass_context=True)
    # async def fuse(self, ctx, pkmn, *args):
    #     """
    #     Fuses all type-specific forms of a pokemon to get the original

    #     @param pkmn - pokemon to fuse into
    #     @param args - enter 5 pokemon to fuse to get to the original
    #                   (valid for only pokemon with over 5 known forms)
    #     """
    #     await self.cmd_function.fuse_pokemon(ctx, pkmn, args)

    # @commands.command(name='exchange', aliases=['e'], pass_context=True)
    # async def exchange(self, ctx, *args):
    #     """
    #     Exchanges 5 pokemon for a pokemon with a 5x shiny chance

    #     @param pkmn - pkmn to be released
    #     """
    #     await self.cmd_function.exchange_pokemon(ctx, args)

    # @commands.command(name='open', aliases=['o'], pass_context=True)
    # async def open(self, ctx, lootbox: str):
    #     """
    #     Opens a lootbox in the inventory

    #     @param lootbox - choices are:
    #                      b - bronze
    #                      s - silver
    #                      g - gold
    #                      l - legendary
    #     """
    #     await self.cmd_function.open_lootbox(ctx, lootbox)

    # @commands.command(name='loot', aliases=['l'], pass_context=True)
    # async def loot(self, ctx):
    #     """
    #     Displays the number of lootboxes the trainer has
    #     """
    #     await self.cmd_function.display_lootbox_inventory(ctx)

    # @commands.command(name='gift', pass_context=True)
    # async def gift(self, ctx):
    #     """
    #     Claims an available gift
    #     """
    #     await self.cmd_function.claim_gift(ctx)