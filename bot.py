from discord.ext import commands
from bot_logger import logger
import json
import logging

COG_MANAGER = "cogs.cog_manager"
with open('config.json') as config:
    config_data = json.load(config)
bot = commands.Bot(command_prefix=config_data["cmd_prefix"],
                   description="Kody's renedition of PokeBot")


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
        if not message.author.bot:
            await bot.process_commands(message)


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
