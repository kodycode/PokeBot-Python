from bot_logger import logger
from discord import Intents
from discord.ext import commands
import asyncio
import json
import logging


COG_MANAGER = "cogs.cog_manager"
CONFIG_JSON_PATH = "bot_config.json"


config_file = open(CONFIG_JSON_PATH)
config_data = json.load(config_file)
intents = Intents(
    dm_messages=True,
    dm_reactions=True,
    emojis=True,
    emojis_and_stickers=True,
    guilds=True,
    members=True,
    messages=True,
    message_content=True,
    reactions=True
)
bot = commands.Bot(command_prefix=config_data["cmd_prefix"],
    description="Renedition of PokeBot",
    intents=intents)


@bot.event
async def on_message(message):
    message.content = message.content.lower()
    if not message.author.bot:
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        # Don't want to reveal admin cmds to regular users
        return
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(content=f"{ctx.message.author.mention},"
                               " please make sure you're entering"
                               " a valid command.")   
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send(content=f"{ctx.message.author.mention},"
                               "Command failed. Please make sure"
                               " you're entering the correct arguments"
                               " for the command.")
    await ctx.send_help(ctx.command)


def main():
    try:
        logger.info('Starting bot..')
        print("Starting bot..")
        asyncio.run(bot.load_extension(COG_MANAGER))
        bot.run(config_data["token"])
    except Exception as e:
        logging.error('Bot failed to run: {}'.format(str(e)))
        print(e)
    logger.info("Bot is now offline.")


main()
