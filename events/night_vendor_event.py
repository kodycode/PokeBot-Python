from collections import defaultdict
from modules import PokeBotEvent


class NightVendorEvent(PokeBotEvent):
    def __init__(self, bot):
        super().__init__(bot, "night_vendor_event")
        self.trainers_reroll_count = {}
        self.vendor_sales = {}
        self.vendor_trade_list = defaultdict(list)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NightVendorEvent, cls).__new__(cls)
            return cls.instance
        return cls.instance

    async def activate(self):
        """
        Activates night vendor event
        """
        if not self.is_active:
            self.is_active = True
            msg = ("**The Night Vendor has arrived! Use the `{0}vendor i` "
                "command for info on what's he's trading. If you're "
                "interested in the trade, type `{0}vendor t` to make. "
                "the trade. If you don't like the roll, type `{0}vendor r` "
                "to re-roll what the vendor has for sale.**"
                "".format(self.bot.command_prefix))
            await self._send_event_start_msg(msg)

    async def deactivate(self):
        """
        Deactivates night vendor event
        """
        self.night_vendor = False
        msg = ("**The night vendor has vanished.**")
        self.vendor_sales.clear()
        self.vendor_trade_list.clear()
        await self._send_event_end_msg(msg)
