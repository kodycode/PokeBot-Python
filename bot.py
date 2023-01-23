from bot_logger import logger
from discord import Intents
from discord.ext import commands
import json
import logging


COG_MANAGER = "cogs.cog_manager"
CONFIG_JSON_PATH = "bot_config.json"


config_file = open(CONFIG_JSON_PATH)
config_data = json.load(config_file)
intents = Intents(
    dm_messages=True,
    dm_reactions=True,
    guilds=True,
    messages=True,
    message_content=True,
    reactions=True
)
bot = commands.Bot(command_prefix=config_data["cmd_prefix"],
    description="Renedition of PokeBot",
    intents=intents)


@bot.event
async def on_ready():
    try:
        await bot.load_extension(COG_MANAGER)
    except Exception as e:
        error_msg = 'Failed to load cog manager\n{}: {}'.format(type(e).__name__, e)
        print(error_msg)
        logger.error(error_msg)


@bot.event
async def on_message(message):
    message.content = message.content.lower()
    if not message.author.bot:
        await bot.process_commands(message)


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await _send_cmd_help(ctx)
    if isinstance(error, commands.errors.BadArgument):
        await _send_cmd_help(ctx)


async def _send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await bot.send_message(ctx.message.channel,
                                "Please make sure you're entering a valid"
                                "command:\n{}".format(page))
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await bot.send_message(ctx.message.channel,
                                "Command failed. Please make sure you're "
                                "entering the correct arguments to the "
                                "command:\n{}".format(page))


def main():
    try:
        logger.info('Starting bot..')
        print("Starting bot..")
        bot.run(config_data["token"])
    except Exception as e:
        logging.error('Bot failed to run: {}'.format(str(e)))
        print(e)
    logger.info("Bot is now offline.")


main()
