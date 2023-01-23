from abc import ABC, abstractmethod
from bot_logger import logger
from database import EventsDAO
import discord


SETTINGS_FOLDER_PATH = "settings"
EVENTS_FOLDER_PATH = f"{SETTINGS_FOLDER_PATH}/events"
HAPPY_HOUR_EVENT_JSON_PATH = f"{EVENTS_FOLDER_PATH}/happy_hour_event.json"
NIGHT_VENDOR_EVENT_JSON_PATH = f"{EVENTS_FOLDER_PATH}/night_vendor_event.json"


class PokeBotEvent(ABC):
    """Generic class to setup PokeBot Events"""

    def __init__(self, bot, event_key: str):
        self.bot = bot
        self.is_active = False
        self.event_data = self._load_event_data(event_key)

    def _load_event_data(self, event_key: str):
        """
        Loads the specific event data given the event key
        """
        try:
            return EventsDAO().get_event(event_key)
        except Exception as e:
            print("ERROR - Exception: {}".format(str(e)))
            logger.error("Exception: {}".format(str(e)))

    async def _send_event_start_msg(self, msg):
        """
        Sends a message to the channel that an event has started

        @param msg - event message to tell the server
        """
        pokemon_channel = ''
        for channel in self.bot.get_all_channels():
            if channel.name == "event":
                pokemon_channel = channel.id
        pokemon_channel_obj = self.bot.get_channel(pokemon_channel)
        em = discord.Embed(title="Event Started",
                           description=msg,
                           colour=0x00FF00)
        await pokemon_channel_obj.send(embed=em)

    async def _send_event_end_msg(self, msg):
        """
        Sends a message to the channel that an event has ended

        @param msg - event message to tell the server
        """
        pokemon_channel = ''
        for channel in self.bot.get_all_channels():
            if channel.name == "event":
                pokemon_channel = channel.id
        pokemon_channel_obj = self.bot.get_channel(pokemon_channel)
        em = discord.Embed(title="Event Ended",
                           description=msg,
                           colour=0xFF0000)
        await pokemon_channel_obj.send(embed=em)

    async def process_event_activation_time(self, hour: int):
        """
        Checks across all events to see if it's time to
        activate or deactivate
        """
        if not self.is_active:
            if hour == self.event_data["event_start_hour"]:
                await self.activate()
        else:
            if hour == self.event_data["event_end_hour"]:
                await self.deactivate()

    @abstractmethod
    async def activate(self):
        """Activates the event (to-be-implemented by chill)"""

    @abstractmethod
    async def deactivate(self):
        """Deactivates the event (to-be-implemented by child)"""
