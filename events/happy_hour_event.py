from modules import PokeBotEvent


class HappyHourEvent(PokeBotEvent):
    def __init__(self, bot, event_key):
        super().__init__(bot, event_key)

    async def activate(self):
        """
        Activates happy hour event
        """
        self.is_active = True
        happy_hour_event = self.happy_hour_event_data["happy_hour_event"]
        msg = (f"**Happy hour has started! During happy "
               "hour, the catch cooldown has "
               "been cut in half, and the shiny rate is {}x higher. "
               "Good luck @everyone!**"
               "".format(happy_hour_event["shiny_rate_multiplier"]))
        await self._send_event_start_msg(msg)

    async def deactivate(self):
        """
        Deactivates happy hour event
        """
        self.is_active = False
        msg = "**Happy hour has ended.**"
        await self._send_event_end_msg(msg)
