from discord.ext import commands
import discord
import re


def format_pokemon_name(pkmn_name: str) -> str:
    formatted_pkmn_name = pkmn_name.replace('_', ' ')
    return formatted_pkmn_name.title()


def get_ctx_user_id(ctx: commands.Context):
    """
    Gets context author user_id returned as string
    """
    return str(ctx.message.author.id)


def get_specific_text_channel(ctx: commands.Context, channel_name: str):
    """
    Gets 'special' channel object
    """
    return discord.utils.get(ctx.message.guild.channels, name=channel_name)


def parse_discord_mention_user_id(user_mention: str):
    """
    Parses discord user ID from mention's extra symbols
    """
    parsed_user_id = re.search(r'\d+', user_mention)
    parsed_user_id = str(parsed_user_id.group(0))
    return parsed_user_id


def is_name_shiny(pkmn_name: str) -> str:
    """
    Checks to see if the pokemon specified has shiny in it
    """
    return pkmn_name.startswith("(shiny)")


def remove_shiny_pokemon_name(pkmn_name: str) -> str:
    """
    Removes the shiny prefix from the pokemon's name
    """
    shiny_removed_pkmn_name = pkmn_name.replace("(shiny)", '')
    return shiny_removed_pkmn_name