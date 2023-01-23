from classes import PokeBotCog
from discord.ext import commands


class NightVendorCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()

    # @commands.command(name='vendor', aliases=['v'], pass_context=True)
    # async def vendor(self, ctx, option: str):
    #     """
    #     Command to communicate with the night vendor

    #     @param options - options include:
    #                      i - info to see what's for sale
    #                      r - re-roll what's for sale
    #                      t - trade the vendor
    #     """
    #     await self.cmd_function.vendor_options(ctx, option)
