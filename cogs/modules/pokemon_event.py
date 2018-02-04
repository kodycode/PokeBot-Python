from bot_logger import logger
import discord
import json


class PokemonEvent:
    """Stores Pokemon Events"""

    def __init__(self, bot, config_data):
        self.bot = bot
        self.config_data = config_data
        self.happy_hour = False
        self.night_vendor = False
        self.event_data = self.load_event_file()

    def load_event_file(self):
        """
        Checks to see if there's a valid events.json file and loads it
        """
        try:
            with open('events.json') as events:
                return json.load(events)
        except FileNotFoundError:
            msg = ("FileNotFoundError: "
                   "'events.json' file was not found")
            logger.error(msg)
            raise Exception(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
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
        await self.bot.send_message(pokemon_channel_obj,
                                    embed=em)

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
        await self.bot.send_message(pokemon_channel_obj,
                                    embed=em)

    async def activate_happy_hour(self):
        """
        Activates happy hour event
        """
        self.happy_hour = True
        happy_hour_event = self.event_data["happy_hour_event"]
        msg = ("**Happy hour has started! During happy "
               "hour, the catch cooldown has "
               "been cut in half, and the shiny rate is {}x higher. "
               "Good luck @everyone!**"
               "".format(happy_hour_event["shiny_rate_multiplier"]))
        await self._send_event_start_msg(msg)

    async def deactivate_happy_hour(self):
        """
        Deactivates happy hour event
        """
        self.happy_hour = False
        msg = "**Happy hour has ended.**"
        await self._send_event_end_msg(msg)

    async def activate_night_vendor(self):
        """
        Activates night vendor event
        """
        self.night_vendor = True
        msg = ("**The Night Vendor has arrived! Use the `{0}vendor i` "
               "command for info on what's he's trading. If you're "
               "interested in the trade, type `{0}vendor t` to make. "
               "the trade. If you don't like the roll, type `{0}vendor r` "
               "to re-roll what the vendor has for sale.**"
               "".format(self.config_data["cmd_prefix"]))
        await self._send_event_start_msg(msg)

    async def deactivate_night_vendor(self):
        """
        Deactivates night vendor event
        """
        self.night_vendor = False
        msg = ("**The night vendor has vanished.**")
        await self._send_event_end_msg(msg)
