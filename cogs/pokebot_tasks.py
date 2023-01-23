from events import EventManager
from modules import PokeBotCog
import asyncio


class PokeBotTasks(PokeBotCog):
    """Runs async tasks for PokeBot that run in a timely manner"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.event_manager = EventManager(bot)
        self.bot.loop.create_task(self._process_all_event_activation_times())

    async def _process_all_event_activation_times(self):
        """
        Checks if it's time for an event and activate it
        """
        while True:
            await self.event_manager.process_all_event_activation_times()
            await asyncio.sleep(60)
