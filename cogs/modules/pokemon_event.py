import discord


class PokemonEvent:
    """Stores Pokemon Events"""

    def __init__(self, bot):
        self.bot = bot
        self.happy_hour = False
        self.happy_hour_cooldown = 5
        self.original_cooldown = None

    async def activate_happy_hour(self, original_cooldown):
        """
        Activates happy hour event
        """
        self.happy_hour = True
        self.original_cooldown = original_cooldown
        pokemon_channel = ''
        for channel in self.bot.get_all_channels():
            if channel.name == "pokemon":
                pokemon_channel = channel.id
        pokemon_channel_obj = self.bot.get_channel(pokemon_channel)
        msg = ("**Happy hour has started! During happy "
               "hour, the catch cooldown has "
               "been cut in half. Good luck trainers!**")
        em = discord.Embed(description=msg,
                           colour=0x00FF00)
        await self.bot.send_message(pokemon_channel_obj,
                                    embed=em)
        return self.happy_hour_cooldown

    async def deactivate_happy_hour(self):
        """
        Deactivates happy hour event
        """
        self.happy_hour = False
        pokemon_channel = ''
        for channel in self.bot.get_all_channels():
            if channel.name == "pokemon":
                pokemon_channel = channel.id
        pokemon_channel_obj = self.bot.get_channel(pokemon_channel)
        msg = "**Happy hour has ended.**"
        em = discord.Embed(description=msg,
                           colour=0xFF0000)
        await self.bot.send_message(pokemon_channel_obj,
                                    embed=em)
        return self.original_cooldown
