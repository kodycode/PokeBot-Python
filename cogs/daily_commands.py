from classes import PokeBotCog


class DailyCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()

    # @commands.command(name='daily', pass_context=True)
    # async def daily(self, ctx):
    #     """
    #     Claim a daily lootbox as well as a daily token
    #     """
    #     await self.cmd_function.claim_daily(ctx)

    # @commands.command(name='tokens', pass_context=True)
    # async def tokens(self, ctx):
    #     """
    #     Displays the number of daily tokens the user has
    #     """
    #     await self.cmd_function.display_daily_tokens(ctx)

    # @commands.command(name='shop', pass_context=True)
    # async def shop(self, ctx, option: str, item_num=None):
    #     """
    #     Displays daily shop

    #     @param options - options include:
    #                      i - info to see what's for sale
    #                      b - buy what's for sale
    #     """
    #     await self.cmd_function.daily_shop(ctx, option, item_num)
