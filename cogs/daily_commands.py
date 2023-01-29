from classes import PokeBotCog
from cogs.logic import DailyLogic
from discord.ext import commands
from modules.pokebot_exceptions import DailyCooldownIncompleteException


class DailyCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()
        self.daily_logic = DailyLogic(bot)

    @commands.command(name='daily', pass_context=True)
    async def daily(self, ctx: commands.Context):
        """
        Claim a daily lootbox as well as a daily token
        """
        try:
            lootbox = self.daily_logic.claim_daily(ctx)
            await ctx.send(f"{ctx.message.author.mention},"
                           f" you've claimed a **{lootbox}** lootbox"
                           " and a daily token to use in the"
                           " daily token shop")
        except DailyCooldownIncompleteException:
            await self.post_daily_cooldown_incomplete_msg(ctx)

    @commands.command(name='tokens', pass_context=True)
    async def tokens(self, ctx: commands.Context):
        """
        Displays the number of daily tokens the user has
        """
        msg = self.daily_logic.build_daily_tokens_msg(ctx)
        await ctx.send(msg)

    # @commands.command(name='shop', pass_context=True)
    # async def shop(self, ctx, option: str, item_num=None):
    #     """
    #     Displays daily shop

    #     @param options - options include:
    #                      i - info to see what's for sale
    #                      b - buy what's for sale
    #     """
    #     await self.cmd_function.daily_shop(ctx, option, item_num)
