from modules import PokeBotEvent


class NightVendorEvent(PokeBotEvent):
    def __init__(self, bot, event_key):
        super().__init__(bot, event_key)

    async def activate(self):
        """
        Activates night vendor event
        """
        self.night_vendor = True
        msg = ("**The Night Vendor has arrived! Use the `{0}vendor i` "
               "command for info on what's he's trading. If you're "
               "interested in the trade, type `{0}vendor t` to make. "
               "the trade. If you don't like the roll, type `{0}vendor r` "
               "to re-roll what the vendor has for sale.**"
               "".format(self.event_data["cmd_prefix"]))
        await self._send_event_start_msg(msg)

    async def deactivate(self):
        """
        Deactivates night vendor event
        """
        self.night_vendor = False
        msg = ("**The night vendor has vanished.**")
        await self._send_event_end_msg(msg)
