from modules.pokebot_cog import PokeBotCog

class NightVendorCommands(PokeBotCog):
    """Handles Pokemon related commands"""
    def __init__(self, bot):
        super().__init__()

    # @commands.command(name='vendor', pass_context=True)
    # async def vendor(self, ctx, option: str):
    #     """
    #     Command to communicate with the night vendor

    #     @param options - options include:
    #                      i - info to see what's for sale
    #                      r - re-roll what's for sale
    #                      t - trade the vendor
    #     """
    #     await self.cmd_function.vendor_options(ctx, option)

    # @commands.command(name='v', pass_context=True, hidden=True)
    # async def v(self, ctx, option: str):
    #     """
    #     Shortcut to communicate with the night vendor

    #     @param options - options include:
    #                      i - info to see what's for sale
    #                      r - re-roll what's for sale
    #                      t - trade the vendor
    #     """
    #     await self.cmd_function.vendor_options(ctx, option)