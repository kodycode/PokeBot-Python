from classes import PokeBotCog
from discord.ext import commands
from cogs.logic.misc_logic import MiscLogic
from modules.pokebot_exceptions import UnregisteredTrainerException


class MiscCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()
        self.misc_logic = MiscLogic(bot)

    @commands.command(name='gif', pass_context=True)
    async def gif(
        self,
        ctx,
        pkmn_name: str = commands.parameter(
            description="The pokemon name to look up."
        ),
        shiny: str = commands.parameter(
            description="Specify 'shiny' or not to look up shiny gif",
            default=None
        )
    ):
        """
        Display a gif of the pokemon
        """
        embed_msg = await self.misc_logic.build_gif_embed(pkmn_name, shiny)
        await ctx.send(embed=embed_msg)

    @commands.command(name='profile', pass_context=True)
    async def profile(
        self,
        ctx: commands.Context,
        user_mention: str = commands.parameter(
            description="The @-mention of the user on disord."
        )
    ) -> None:
        """
        Obtains the profile of a trainer specified
        """
        try:
            embed_msg = await self.misc_logic.build_trainer_profile_msg(
                ctx,
                user_mention
            )
            await ctx.send(embed=embed_msg)
        except UnregisteredTrainerException:
            await self.post_unregistered_trainer_exception_msg(ctx)
