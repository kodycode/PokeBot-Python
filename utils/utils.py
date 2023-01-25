from discord.ext import commands
import discord


def format_pokemon_name(pkmn_name: str) -> str:
    return pkmn_name.replace('_', ' ').title()


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
