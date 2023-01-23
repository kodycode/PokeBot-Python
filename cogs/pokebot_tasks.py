from bot_logger import logger
from events import HappyHourEvent, NightVendorEvent
from modules import PokeBotCog
import datetime
import asyncio


class PokeBotTasks(PokeBotCog):
    """Runs async tasks for PokeBot that run in a timely manner"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.events = [
            HappyHourEvent(bot),
            NightVendorEvent(bot)
        ]
        self.bot.loop.create_task(self._process_all_event_activation_times())

    async def _process_all_event_activation_times(self):
        """
        Checks if it's time for an event and activate it
        """
        while True:
            hour = int(datetime.datetime.now().hour)
            for event in self.events:
                await event.process_event_activation_time(hour)
            await asyncio.sleep(60)
