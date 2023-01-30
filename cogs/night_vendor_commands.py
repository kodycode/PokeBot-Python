from classes import PokeBotCog
from cogs.logic import NightVendorLogic
from discord.ext import commands
from events import EventManager
from modules.pokebot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    NotEnoughRerollsException
)


class NightVendorCommands(PokeBotCog):

    def __init__(self, bot):
        super().__init__()
        self.event_manager = EventManager(bot)
        event = self.event_manager.get_event_by_key("night_vendor")
        self.nv = NightVendorLogic(
            bot,
            event
        )

    def _is_event_active(self) -> bool:
        """
        Checks if the event is active
        """
        return self.event_manager.is_event_active("night_vendor")

    async def _post_night_vendor_inactive_msg(
        self,
        ctx: commands.Context
    ) -> None:
        """
        Posts the message specifying that the night vendor is away
        """
        await ctx.send("Night Vendor is currently away.")

    @commands.command(name='nv', pass_context=True)
    async def nv(self, ctx: commands.Context) -> None:
        """
        Displays what the night vendor wants to trade
        """
        if self._is_event_active():
            msg = self.nv.build_night_vendor_offer_msg(ctx)
            await ctx.send(msg)
        else:
            await self._post_night_vendor_inactive_msg()

    @commands.command(name='nvroll', pass_context=True)
    async def nvroll(self, ctx: commands.Context) -> None:
        """
        Re-rolls what the night vendor has to offer
        """
        try:
            if self._is_event_active():
                self.nv.reroll_night_vendor_offer(ctx)
                msg = self.nv.build_night_vendor_offer_msg(ctx)
                await ctx.send(msg)
            else:
                await self._post_night_vendor_inactive_msg()
        except NotEnoughRerollsException:
            await self.post_not_enough_reroll_exception_msg(ctx)

    @commands.command(name='nvtrade', pass_context=True)
    async def nvtrade(self, ctx: commands.Context) -> None:
        """
        Confirms the night vendor trade
        """
        try:
            if self._is_event_active():
                self.nv.trade_night_vendor(ctx)
            else:
                await self._post_night_vendor_inactive_msg()
        except HigherReleaseQuantitySpecifiedException:
            await self.post_higher_quantity_specified_exception_msg()
