from classes import PokeBotCog
from discord.ext import commands, tasks
from events import EventManager
import asyncio


class PokeBotTasks(PokeBotCog):
    """Runs async tasks for PokeBot that run in a timely manner"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.event_manager = EventManager(bot)
        self._process_all_event_activation_times.start()

    @tasks.loop(seconds=60.0)
    async def _process_all_event_activation_times(self):
        """
        Checks if it's time for an event and activate it
        """
        await self.event_manager.process_all_event_activation_times()
