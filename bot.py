from discord.ext import commands
from bot_logger import logger
import json
import logging

COG_MANAGER = "cogs.cog_manager"
with open('config.json') as config:
    config_data = json.load(config)
bot = commands.Bot(command_prefix=config_data["cmd_prefix"],
                   description="Renedition of PokeBot")


class PokeBot:
    """Initiates the Bot"""

    def __init__(self):
        bot.run(config_data["token"])

    @bot.event
    async def on_ready():
        try:
            bot.load_extension(COG_MANAGER)
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
            await send_cmd_help(ctx)
        if isinstance(error, commands.errors.BadArgument):
            await send_cmd_help(ctx)


async def send_cmd_help(ctx):
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
        PokeBot()
    except Exception as e:
        logging.error('Bot failed to run: {}'.format(str(e)))
        print(e)
    logger.info("Bot is now offline.")


main()
