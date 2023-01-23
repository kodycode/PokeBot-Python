from modules import PokeBotEvent


class HappyHourEvent(PokeBotEvent):
    def __init__(self, bot):
        super().__init__(bot, "happy_hour_event")

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HappyHourEvent, cls).__new__(cls)
            return cls.instance
        return cls.instance

    async def activate(self):
        """
        Activates happy hour event
        """
        if not self.is_active:
            self.is_active = True
            msg = (f"**Happy hour has started! During happy "
                "hour, the catch cooldown has "
                "been cut in half, and the shiny rate is {}x higher. "
                "Good luck @everyone!**"
                "".format(self.event_data["shiny_rate_multiplier"]))
            await self._send_event_start_msg(msg)

    async def deactivate(self):
        """
        Deactivates happy hour event
        """
        self.is_active = False
        msg = "**Happy hour has ended.**"
        await self._send_event_end_msg(msg)
