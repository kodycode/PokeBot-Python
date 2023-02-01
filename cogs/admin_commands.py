# from modules.pokemon_functionality import PokemonFunctionality
from classes import PokeBotCog
from cogs.logic.admin_logic import AdminLogic
from discord.ext import commands
from modules.pokebot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    LootboxDoesNotExistException,
    NotEnoughLootboxQuantityException,
    PokemonDoesNotExistException,
    UnregisteredTrainerException
)
from utils.utils import format_shiny_pokemon_name, is_name_shiny


class AdminCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()
        self.admin_logic = AdminLogic(bot)

    @commands.command(name='give', pass_context=True, hidden=True)
    @commands.has_role('PokeBot Admin')
    async def give(
        self,
        ctx: commands.Context, 
        user_id: int=commands.parameter(
            description="ID of the trainer to give a pokemon too"
        ),
        pkmn_name: str=commands.parameter(
            description="Name of the pokemon to delete"
        ),
        shiny: str=commands.parameter(
            description="Specify 's' or not to give a shiny pokemon",
            default=''
        )
    ) -> None:
        """
        Gives a pokemon to a trainer (admin only cmd)
        """
        try:
            is_shiny = False
            if shiny == 's':
                is_shiny = True
            str_user_id = str(user_id)
            await self.admin_logic.give_pokemon(
                str_user_id,
                pkmn_name,
                is_shiny
            )
            formatted_pkmn_name = pkmn_name.title()
            if is_shiny:
                formatted_pkmn_name = "(Shiny) " + formatted_pkmn_name
            await ctx.send(f"{ctx.message.author.mention} gave a"
                           f" **{formatted_pkmn_name}** to <@{str_user_id}>")
        except PokemonDoesNotExistException as e:
            await self.post_pokemon_does_not_exist_exception_msg(ctx, e)

    @commands.command(name='delete', pass_context=True, hidden=True)
    @commands.has_role('PokeBot Admin')
    async def delete(
        self,
        ctx: commands.Context,
        user_id: int=commands.parameter(
            description="ID of the trainer to give a pokemon too"
        ),
        pkmn_name: str=commands.parameter(
            description=("Name of the pokemon to delete i.e. "
                         "'pikachu', '(shiny)pikachu'")
        )
    ) -> None:
        """
        Deletes a pokemon from the trainer (admin only cmd)
        """
        try:
            str_user_id = str(user_id)
            formatted_pkmn_name = pkmn_name.lower()
            await self.admin_logic.delete_pokemon(str_user_id,
                                                  formatted_pkmn_name)
            if is_name_shiny(pkmn_name):
                formatted_pkmn_name = format_shiny_pokemon_name(pkmn_name)
            else:
                formatted_pkmn_name = formatted_pkmn_name.title()
            await ctx.send(f"{ctx.message.author.mention} deleted a" \
                           f" **{formatted_pkmn_name}** from trainer" \
                           f" <@{str_user_id}>")
        except UnregisteredTrainerException as e:
            await self.post_unregistered_trainer_admin_exception_msg(ctx, e)
        except HigherReleaseQuantitySpecifiedException as e:
            await self.post_higher_quantity_specified_exception_msg(ctx, e)
        except PokemonDoesNotExistException as e:
            await self.post_pokemon_does_not_exist_exception_msg(ctx, e)

    @commands.command(name='giveloot', pass_context=True, hidden=True)
    @commands.has_role('PokeBot Admin')
    async def giveloot(
        self,
        ctx: commands.Context,
        user_id: int=commands.parameter(
            description="ID of the trainer to give a pokemon too"
        ),
        lootbox: str=commands.parameter(
            description="Specify either 'bronze', 'silver' or 'gold' lootbox"
        )
    ) -> None:
        """
        Gives a trainer a specified lootbox
        """
        try:
            str_user_id = str(user_id)
            formatted_lootbox = lootbox.lower()
            await self.admin_logic.give_lootbox(str_user_id,
                                                formatted_lootbox)
            await ctx.send(f"{ctx.message.author.mention} gave a" \
                           f" **{formatted_lootbox.title()}** lootbox" \
                           f" to trainer <@{str_user_id}>")
        except LootboxDoesNotExistException as e:
            await self.post_lootbox_does_not_exist(ctx, e)

    @commands.command(name='deleteloot', pass_context=True, hidden=True)
    @commands.has_role('PokeBot Admin')
    async def deleteloot(
        self,
        ctx: commands.Context,
        user_id: int=commands.parameter(
            description="ID of the trainer to give a pokemon too"
        ),
        lootbox: str=commands.parameter(
            description="Specify either 'bronze', 'silver' or 'gold' lootbox"
        )
    ) -> None:
        """
        Deletes a lootbox from a trainer's inventory
        """
        try:
            str_user_id = str(user_id)
            formatted_lootbox = lootbox.lower()
            await self.admin_logic.delete_lootbox(str_user_id,
                                                formatted_lootbox)
            await ctx.send(f"{ctx.message.author.mention} deleted a" \
                           f" **{formatted_lootbox.title()}** lootbox from" \
                           f" trainer <@{str_user_id}>")
        except UnregisteredTrainerException as e:
            await self.post_unregistered_trainer_admin_exception_msg(ctx, e)
        except LootboxDoesNotExistException as e:
            await self.post_lootbox_does_not_exist(ctx, e)
        except NotEnoughLootboxQuantityException as e:
            await self.post_not_enough_lootbox_quantity_admin_exception_msg(
                ctx,
                e
            )
