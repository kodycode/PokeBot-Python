# **NOTE: NOT TAKING ANY FEATURE REQUESTS OR REQUESTS FOR ADDITIONAL MECHANICS**

I made this bot 5 years ago (Jan 2018) for me and a couple of friends. We no longer use this bot, hence this project is now just used as a means to exercise my current coding knowledge and as a means to learn. It was in a rough shape from when I started years ago, and as of 01/01/2023, I'm releasing an updated version with an improved codebase. There may be questionable design choices, such as the use of JSON files as storage, but from when I started 5 years ago, I didn't need a more advanced storage to use between 3 other friends and I as performance was never affected by how often these files were read/written. Later down the line I might implement the use of one, and I've setup the scenario to do so with the existance of the DAO files underneath `database/`, but no guarantee given my time and interest with the project.

That being said, **this bot is meant to be used within a small discord server and may have its performance impacted in bigger server(s). While I'm not taking anymore feature requests, I am taking any bugs and issues that occur with the bot**. I don't have a lot of time, though should I have any, I may investigate these bugs and put up a fix for them.

------------

# Description

Made with Python 3.9 and the [Python Discord API Wrapper](https://github.com/Rapptz/discord.py) while pertaining to Flake8 standards with <120 characters per line of code.

This bot focuses on the catching aspect that was developed by the original [PokéBot](https://discordbots.org/bot/330488924449275916?utm_source=widget). While it contains the similar style of catching pokemon from the original, I've added more tweaks of my own. You can hatch and exchange pokemon, and even get lootboxes containing pokemon. You can also customize the bot to have events.

To read more on the bot's features, see the [command page](https://github.com/kodycode/PokeBot-Python/wiki/Command-Page).

For information on current events, see the [event page](https://github.com/kodycode/PokeBot-Python/wiki/Events).

# Installation

To setup the bot,

1. Run `pip install -r requirements.txt`

1. Enter your discord bot token into the `token` field of bot_config.json

1. Run the bot with `python bot.py` or `python3 bot.py`

For more options for configuration, see the [config page](https://github.com/kodycode/PokeBot-Python/wiki/Config).

# Pull Requests

**I'm not taking any pull requests unless these pull requests pertain to improving the current code.**

# Disclaimer
**This in no way is meant to compete with the official [PokéBot](https://discordbots.org/bot/330488924449275916?utm_source=widget). This renedition was purely made for my own benefit and for my own server. Pokémon assets belong to Wonder & Toast and can be found [here](https://github.com/Wonder-Toast/Pokemon-PNG). Pokéball assets that were not included in this repo, can be found [here](https://github.com/msikma/pokesprite).<br><br>Credits to nintendo wikia for the ultra beasts pictures.**
