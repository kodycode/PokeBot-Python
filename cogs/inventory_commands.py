# from cogs.modules.pokemon_functionality import PokemonFunctionality
from classes import PokeBotCog
from discord.ext import commands
from modules import InventoryLogic
from modules.pokebot_exceptions import (
    HigherPageSpecifiedException,
    HigherReleaseQuantitySpecifiedException,
    PageQuantityTooLow,
    ReleaseQuantityTooLow,
    UnregisteredTrainerException,
)


class InventoryCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()
        self.inventory_logic = InventoryLogic(bot)

    @commands.command(name='catch', aliases=['c'], pass_context=True)
    async def catch(self, ctx: commands.Context):
        """
        Catches a random pokemon and gives it to the trainer
        """
        await self.inventory_logic.catch_pokemon(ctx)

    @commands.command(name='inventory', aliases=['i'], pass_context=True)
    async def pinventory(
        self,
        ctx: commands.Context,
        page: int=commands.parameter(
            description="The @-mention of the user on disord.",
            default=1
        )
    ):
        """
        Displays the trainer's pokemon inventory
        """
        try:
            if page < 1:
                raise PageQuantityTooLow()
            await self.inventory_logic.display_pinventory(ctx, page)
        except HigherPageSpecifiedException as e:
            await self._post_higher_page_specified_exception_msg(ctx, e)
        except PageQuantityTooLow:
            await self._post_page_quantity_too_low_msg(ctx)
        except UnregisteredTrainerException:
            await self._post_unregistered_trainer_exception_msg(ctx)

    @commands.command(name='release', aliases=['r'], pass_context=True)
    async def release(
        self,
        ctx: commands.Context,
        pkmn_name: str=commands.parameter(
            description="The name of the pokemon"
        ),
        quantity=1
    ):
        """
        Releases a pokemon from your inventory
        """
        try:
            if quantity <= 0:
                raise ReleaseQuantityTooLow()
            await self.inventory_logic.release_pokemon(
                ctx,
                pkmn_name,
                quantity,
            )
            await ctx.send(f"{ctx.message.author.mention} "
                           f"successfully released {pkmn_name.title()}")
        except HigherReleaseQuantitySpecifiedException as e:
            await self._post_higher_quantity_specified_exception_msg(ctx, e)
        except ReleaseQuantityTooLow as e:
            await self._post_release_quantity_too_low_msg(ctx, e)

    # @commands.command(name='hatch', aliases=['h'], pass_context=True)
    # async def hatch(self, ctx):
    #     """
    #     Hatches an egg from your inventory

    #     @param pkmn - pkmn to be released
    #     """
    #     await self.cmd_function.hatch_egg(ctx)

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

    # @commands.command(name='claim', pass_context=True)
    # async def claim(self, ctx):
    #     """
    #     Claims an available gift
    #     """
    #     await self.cmd_function.claim_gift(ctx)
