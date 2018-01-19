from bot_logger import logger
import discord
import json


class PokemonEvent:
    """Stores Pokemon Events"""

    def __init__(self, bot):
        self.bot = bot
        self.happy_hour = False
        self.event_data = self.check_event_file()

    def check_event_file(self):
        """
        Checks to see if there's a valid events.json file
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

    async def activate_happy_hour(self):
        """
        Activates happy hour event
        """
        pokemon_channel = ''
        for channel in self.bot.get_all_channels():
            if channel.name == "pokemon":
                pokemon_channel = channel.id
        pokemon_channel_obj = self.bot.get_channel(pokemon_channel)
        msg = ("**Happy hour has started! During happy "
               "hour, the catch cooldown has "
               "been cut in half. Good luck @everyone!**")
        em = discord.Embed(title="Event Started",
                           description=msg,
                           colour=0x00FF00)
        await self.bot.send_message(pokemon_channel_obj,
                                    embed=em)
        self.happy_hour = True

    async def deactivate_happy_hour(self):
        """
        Deactivates happy hour event
        """
        pokemon_channel = ''
        for channel in self.bot.get_all_channels():
            if channel.name == "pokemon":
                pokemon_channel = channel.id
        pokemon_channel_obj = self.bot.get_channel(pokemon_channel)
        msg = "**Happy hour has ended.**"
        em = discord.Embed(title="Event Ended",
                           description=msg,
                           colour=0xFF0000)
        await self.bot.send_message(pokemon_channel_obj,
                                    embed=em)
        self.happy_hour = False
