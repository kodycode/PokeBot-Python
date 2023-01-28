# from cogs.modules.pokemon_functionality import PokemonFunctionality
from classes import PokeBotCog
from discord.ext import commands
from modules import InventoryLogic
from modules.pokebot_exceptions import (
    CatchCooldownIncompleteException,
    HigherPageSpecifiedException,
    HigherReleaseQuantitySpecifiedException,
    NoEggCountException,
    NotEnoughExchangePokemonQuantityException,
    NotEnoughExchangePokemonSpecifiedException,
    NotEnoughLootboxQuantityException,
    PageQuantityTooLow,
    ReleaseQuantityTooLow,
    TooManyExchangePokemonSpecifiedException,
    UnregisteredTrainerException,
)


class InventoryCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()
        self.inventory_logic = InventoryLogic(bot)

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        await self.inventory_logic._display_total_pokemon_caught()

    @commands.command(name='catch', aliases=['c'], pass_context=True)
    async def catch(self, ctx: commands.Context):
        """
        Catches a random pokemon and gives it to the trainer
        """
        try:
            await self.inventory_logic.catch_pokemon(ctx)
        except CatchCooldownIncompleteException as e:
            await self.post_catch_cooldown_incomplete_msg(ctx, e)

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
            embed_msg = \
                await self.inventory_logic.build_pinventory_msg(ctx, page)
            await ctx.send(embed=embed_msg)
        except HigherPageSpecifiedException as e:
            await self.post_higher_page_specified_exception_msg(ctx, e)
        except PageQuantityTooLow:
            await self.post_page_quantity_too_low_msg(ctx)
        except UnregisteredTrainerException:
            await self.post_unregistered_trainer_exception_msg(ctx)

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
            await self.post_higher_quantity_specified_exception_msg(ctx, e)
        except ReleaseQuantityTooLow as e:
            await self.post_release_quantity_too_low_msg(ctx, e)

    @commands.command(name='eggs', aliases=['e'], pass_context=True)
    async def eggs(self, ctx: commands.Context) -> None:
        """
        Gets the number of eggs that the trainer has
        """
        try:
            embed_msg = await self.inventory_logic.build_eggs_msg(ctx)
            await ctx.send(embed=embed_msg)
        except UnregisteredTrainerException:
            await self.post_unregistered_trainer_exception_msg()

    @commands.command(name='hatch', aliases=['h'], pass_context=True)
    async def hatch(
        self,
        ctx: commands.Context,
        special_egg: str=commands.parameter(
            description="Specify 'm' to hatch a manaphy egg if you have one",
            default=''
        )
    ):
        """
        Hatches an egg from your inventory
        """
        try:
            await self.inventory_logic.hatch_egg(ctx, special_egg)
        except NoEggCountException as e:
            await self.post_no_egg_count_msg(ctx, e)
        except UnregisteredTrainerException:
            await self.post_unregistered_trainer_exception_msg(ctx)

    @commands.command(name='exchange', pass_context=True)
    async def exchange(
        self,
        ctx:commands.Context,
        *args: str
    ) -> None:
        """
        Exchanges 5 pokemon for a pokemon with a modified shiny chance
        rate
        
        Example usage:
        !exchange pikachu pikachu charizard squirtle bulbasaur
        """
        try:
            await self.inventory_logic.exchange_pokemon(ctx, *args)
        except NotEnoughExchangePokemonQuantityException:
            await self.post_not_enough_exchange_pokemon_quantity_exception(
                ctx
            )
        except NotEnoughExchangePokemonSpecifiedException:
            await self.post_not_enough_exchange_pokemon_specified_exception(
                ctx
            )
        except TooManyExchangePokemonSpecifiedException:
            await self.post_too_many_exchange_pokemon_specified_exception(
                ctx
            )
        except UnregisteredTrainerException:
            await self.post_unregistered_trainer_exception_msg(ctx)

    @commands.command(name='open', aliases=['o'], pass_context=True)
    async def open(
        self,
        ctx:commands.Context,
        lootbox: str=commands.parameter(
            description="Specify either a 'bronze', 'silver', or 'gold' lootbox to open"
        )
    ):
        """
        Opens a specified lootbox in the inventory
        """
        try:
            embed_msg = await self.inventory_logic.open_lootbox(ctx, lootbox)
            await ctx.send(embed=embed_msg)
        except NotEnoughLootboxQuantityException as e:
            await self.post_not_enough_lootbox_quantity_exception_msg(ctx, e)
        except UnregisteredTrainerException:
            await self.post_unregistered_trainer_exception_msg(ctx)

    @commands.command(name='loot', aliases=['l'], pass_context=True)
    async def loot(self, ctx: commands.Context):
        """
        Displays the number of lootboxes the trainer has
        """
        try:
            embed_msg = \
                await self.inventory_logic.display_lootbox_inventory(ctx)
            await ctx.send(embed=embed_msg)
        except UnregisteredTrainerException:
            await self.post_unregistered_trainer_exception_msg(ctx)
