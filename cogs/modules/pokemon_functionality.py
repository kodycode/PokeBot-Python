from bot_logger import logger
from cogs.modules.pokemon_event import PokemonEvent
from collections import defaultdict
from discord import File
from math import ceil
from operator import itemgetter
import asyncio
import datetime
import discord
import glob
import json
import os
import random
import re
import time

SETTINGS_FOLDER_PATH = "settings"
CONFIG_JSON_PATH = f"{SETTINGS_FOLDER_PATH}/config.json"
DAILY_JSON_PATH = f"{SETTINGS_FOLDER_PATH}/daily.json"
GIFT_JSON_PATH = f"{SETTINGS_FOLDER_PATH}/gift.json"
LEGENDARY_PKMN_JSON_PATH = f"{SETTINGS_FOLDER_PATH}/legendary_pkmn.json"
POKEBALLS_JSON_PATH = f"{SETTINGS_FOLDER_PATH}/pokeballs.json"
TRAINERS_JSON_PATH = f"{SETTINGS_FOLDER_PATH}/trainers.json"
TRAINERS_BACKUP_JSON_PATH = f"{SETTINGS_FOLDER_PATH}/trainers_backup.json"
ULTRA_BEASTS_JSON_PATH = f"{SETTINGS_FOLDER_PATH}/ultra_beasts.json"

BRONZE = "bronze"
SILVER = "silver"
GOLD = "gold"
LEGEND = "legendary"

BRONZE_LOOTBOX_PRICE = 3
SILVER_LOOTBOX_PRICE = 6
GOLD_LOOTBOX_PRICE = 9
LEGENDARY_LOOTBOX_PRICE = 15
RANDOM_SHINY_PRICE = 50


SHINY_ICON_URL = "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/shiny/"
SHINY_GIF_URL = "https://play.pokemonshowdown.com/sprites/xyani-shiny/"
NRML_ICON_URL = "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/"
NRML_GIF_URL = "https://play.pokemonshowdown.com/sprites/xyani/"


class PokemonFunctionality:
    """Handles Pokemon Command Functionality"""

    def __init__(self, bot):
        self.bot = bot
        self.trainer_cache = {}
        self.vendor_sales = {}
        self.vendor_trade_list = defaultdict(list)
        self.config_data = self._load_config_file()
        self.legendary_pkmn = self._load_legendary_file()
        self.ultra_beasts = self._load_ultra_file()
        self.pokeball = self._load_pokeball_file()
        self.event = PokemonEvent(bot, self.config_data)
        self.nrml_pokemon = self._load_pokemon_imgs()
        self.shiny_pokemon = self._load_pokemon_imgs(shiny=True)
        self.daily_data = self._load_daily_file()
        self.gift_data = self._load_gift_file()
        self.trainer_data = self._load_trainer_file()
        self._save_trainer_file(self.trainer_data, backup=True)
        self.bot.loop.create_task(self._update_cache())
        self.bot.loop.create_task(self._display_total_pokemon_caught())
        self.bot.loop.create_task(self._load_event())
        self.bot.loop.create_task(self._refresh_daily())

    async def update_game_status(self, total_pkmn_count):
        """
        Updates the game status of the bot
        """
        try:
            game_status = discord.Game(name="{} Pokémon caught"
                                            "".format(total_pkmn_count))
            await self.bot.change_presence(activity=game_status)
        except Exception as e:
            print("Failed to update game status. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def _cache_users(self):
        """
        Caches user data based on the trainers in trainers.json
        """
        try:
            trainer_cache = {}
            for trainer in self.trainer_data:
                user_obj = await self.bot.fetch_user(str(trainer))
                trainer_cache[trainer] = user_obj
            self.trainer_cache = trainer_cache
        except Exception as e:
            print("Failed to cache trainer object. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def _update_cache(self):
        """
        Calls function to cache user objects every hour
        """
        while True:
            await self._cache_users()
            await asyncio.sleep(3600)

    async def _refresh_daily(self):
        """
        Checks and refreshes the daily
        """
        while True:
            hour = int(datetime.datetime.now().hour)
            if hour == self.config_data["daily_reset_hour"]:
                self._save_daily_file([])
                self.daily_data = self._load_daily_file()
                await asyncio.sleep(3600)
            await asyncio.sleep(60)

    async def _display_total_pokemon_caught(self):
        """
        Iterates over trainer profiles and gets the total
        number of pokemon caught
        """
        try:
            total_pokemon_caught = 0
            for trainer in self.trainer_data:
                pinventory = self.trainer_data[trainer]["pinventory"]
                for pkmn in pinventory:
                    total_pokemon_caught += pinventory[pkmn]
            await self.update_game_status(total_pokemon_caught)
        except Exception as e:
            print("Failed to get total pokemon caught. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def _load_event(self):
        """
        Checks if it's time for an event and activates it if it is
        """
        while True:
            hour = int(datetime.datetime.now().hour)
            happy_hour_event = self.event.happy_hour_event_data
            night_vendor_event = self.event.night_vendor_event_data
            if happy_hour_event["event"]:
                if hour == happy_hour_event["event_start_hour"]:
                    await self.event.activate_happy_hour()
                    await asyncio.sleep(happy_hour_event["duration"])
                    await self.event.deactivate_happy_hour()
            if night_vendor_event["event"]:
                if hour == night_vendor_event["event_start_hour"]:
                    reroll_count = night_vendor_event["reroll_count"]
                    for trainer in self.trainer_data:
                        trainer_profile = self.trainer_data[trainer]
                        trainer_profile["reroll_count"] = reroll_count
                    self._save_trainer_file(self.trainer_data)
                    await self.event.activate_night_vendor()
                    await asyncio.sleep(night_vendor_event["duration"])
                    await self.event.deactivate_night_vendor()
                    self.vendor_sales.clear()
                    self.vendor_trade_list.clear()
            await asyncio.sleep(60)

    def _load_config_file(self):
        """
        Checks to see if there's a valid config.json file and loads it
        """
        try:
            with open(CONFIG_JSON_PATH) as config:
                return json.load(config)
        except FileNotFoundError:
            msg = f"FileNotFoundError: {CONFIG_JSON_PATH} file not found"
            print(msg)
            logger.error(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _load_legendary_file(self):
        """
        Checks to see if there's a valid legendary_pkmn.json file and loads it
        """
        try:
            with open(LEGENDARY_PKMN_JSON_PATH) as legendaries:
                return json.load(legendaries)
        except FileNotFoundError:
            msg = f"FileNotFoundError: {LEGENDARY_PKMN_JSON_PATH} file not found"
            print(msg)
            logger.error(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _load_ultra_file(self):
        """
        Checks to see if there's a valid ultra_beasts.json file
        """
        try:
            with open(ULTRA_BEASTS_JSON_PATH) as ultras:
                return json.load(ultras)
        except FileNotFoundError:
            msg = f"FileNotFoundError: {ULTRA_BEASTS_JSON_PATH} file not found"
            print(msg)
            logger.error(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _load_pokeball_file(self):
        """
        Checks to see if there's a valid pokeballs.json file and loads it
        """
        try:
            with open(POKEBALLS_JSON_PATH) as pokeballs:
                return json.load(pokeballs)
        except FileNotFoundError:
            msg = f"FileNotFoundError: {POKEBALLS_JSON_PATH} file not found"
            print(msg)
            logger.error(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _load_trainer_file(self):
        """
        Checks to see if there's a valid trainers.json file and loads it
        """
        try:
            with open(TRAINERS_JSON_PATH) as trainers:
                return json.load(trainers)
        except FileNotFoundError:
            self._save_trainer_file()
            return json.loads('{}')
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _load_daily_file(self):
        """
        Checks to see if there's a valid daily.json file and loads it
        """
        try:
            with open(DAILY_JSON_PATH) as daily:
                return json.load(daily)
        except FileNotFoundError:
            self._save_daily_file([])
            return json.loads('[]')
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _load_gift_file(self):
        """
        Checks to see if there's a valid gift.json file and loads it
        """
        try:
            with open(GIFT_JSON_PATH) as gift:
                return json.load(gift)
        except FileNotFoundError:
            self._save_gift_file([])
            return json.loads('[]')
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _save_daily_file(self, daily_data={}):
        """
        Saves daily.json file
        """
        daily_filename = "daily.json"
        with open(daily_filename, 'w') as outfile:
            json.dump(daily_data,
                      outfile,
                      indent=4)

    def _save_gift_file(self, gift_data={}):
        """
        Saves gift.json file
        """
        gift_filename = "gift.json"
        with open(gift_filename, 'w') as outfile:
            json.dump(gift_data,
                      outfile,
                      indent=4)

    def _save_trainer_file(self, trainer_data={}, backup=False):
        """
        Saves trainers.json file
        """
        if backup:
            trainer_filename = TRAINERS_BACKUP_JSON_PATH
        else:
            trainer_filename = TRAINERS_JSON_PATH
        with open(trainer_filename, 'w') as outfile:
            json.dump(trainer_data,
                      outfile,
                      indent=4)

    def _load_pokemon_imgs(self, shiny=False):
        """
        Loads pokemon images within a folder

        Note: Make path universal
        """
        filedict = defaultdict(list)
        if shiny:
            folder_path = os.path.join('assets', 'shiny')
            img_path = os.path.join('assets', 'shiny', '*.png')
        else:
            folder_path = os.path.join('assets', 'nrml')
            img_path = os.path.join('assets', 'nrml', '*.png')
        for filename in glob.glob(img_path):
            result = re.match(r'([^\d]+)', filename)
            if result:
                pkmn_name = filename.lower()
                pkmn_name = pkmn_name.replace(folder_path, "")
                pkmn_name = pkmn_name.replace('/', "")
                pkmn_name = pkmn_name.replace('\\', "")
                pkmn_name = pkmn_name.replace('.png', "")
                filedict[pkmn_name].append(filename)
        return filedict

    async def _valid_user(self, ctx, user_id):
        """
        Checks if the valid is user

        @return - true if valid,
                  false if invalid
        """
        if not self.trainer_cache:
            await ctx.send("Trainer data is still loading. "
                           "Please wait and try again later.")
            return False
        elif user_id not in self.trainer_data:
            await ctx.send("Trainer hasn't set off on his journey to "
                           "catch 'em all yet. (Catch a pokemon first in "
                           "order to use this bot command).")
            return False
        return True

    async def give_trainer_pokemon(self, ctx, user_id, pkmn_name, shiny):
        """
        Gives a pokemon to the trainer
        """
        try:
            admin_id = str(ctx.message.author.id)
            if admin_id in self.config_data["admin_list"]:
                if user_id in self.trainer_data:
                    trainer_profile = self.trainer_data[user_id]
                else:
                    await ctx.send("Trainer ID was not found.")
                    return
                if pkmn_name in self.nrml_pokemon:
                    if shiny == "s" or shiny == "shiny":
                        if pkmn_name in self.shiny_pokemon:
                            shiny = True
                        else:
                            await ctx.send("This pokemon does not have a "
                                           "shiny version available: **{}**"
                                           "".format(pkmn_name.title()))
                            return
                    else:
                        shiny = False
                    self._move_pokemon_to_inventory(trainer_profile,
                                                    pkmn_name,
                                                    shiny)
                    self._save_trainer_file(self.trainer_data)
                    msg = ("<@{}> gave <@{}> a/an **{}**"
                           "".format(admin_id,
                                     user_id,
                                     pkmn_name.title()))
                    if shiny:
                        msg += (" **(Shiny)**")
                    await ctx.send(msg)
                else:
                    await ctx.send("Invalid pokemon: **{}**"
                                   "".format(pkmn_name.title()))
        except Exception as e:
            error_msg = 'Failed to give user a lootbox: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def delete_trainer_pokemon(self, ctx, user_id, pkmn_name, shiny):
        """
        Deletes a pokemon specified from the trainer's inventory
        """
        try:
            admin_id = ctx.message.author.id
            if admin_id in self.config_data["admin_list"]:
                if user_id in self.trainer_data:
                    trainer_profile = self.trainer_data[user_id]
                else:
                    await ctx.send("Trainer ID was not found.")
                    return
                pinventory = trainer_profile["pinventory"]
                if pkmn_name in pinventory:
                    if shiny == "s" or shiny == "shiny":
                        pkmn_name += "(Shiny)"
                    successful = await self.release_pokemon(ctx,
                                                            pkmn_name,
                                                            1,
                                                            True,
                                                            False)
                    if not successful:
                        return
                    msg = ("<@{}> deleted **{}** from <@{}>'s inventory"
                           "".format(admin_id,
                                     pkmn_name.title(),
                                     user_id))
                    await ctx.send(msg)
                else:
                    await ctx.send("Invalid pokemon: **{}**"
                                   "".format(pkmn_name.title()))
        except Exception as e:
            error_msg = 'Failed to delete a pokemon from the user: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def give_trainer_lootbox(self, ctx, user_id, lootbox):
        """
        Gives a lootbox to a user based on their ID

        @param ctx - context of the command sent
        @param user_id - user to give pokemon to
        @param lootbox - lootbox to give to the user
        """
        try:
            admin_id = ctx.message.author.id
            if admin_id in self.config_data["admin_list"]:
                if user_id in self.trainer_data:
                    trainer_profile = self.trainer_data[user_id]
                else:
                    await ctx.send("Trainer ID was not found.")
                    return
                if lootbox == "b":
                    self._move_lootbox_to_inventory(trainer_profile,
                                                    bronze=True)
                    lootbox = BRONZE
                elif lootbox == "s":
                    self._move_lootbox_to_inventory(trainer_profile,
                                                    silver=True)
                    lootbox = SILVER
                elif lootbox == "g":
                    self._move_lootbox_to_inventory(trainer_profile,
                                                    gold=True)
                    lootbox = GOLD
                elif lootbox == "l":
                    self._move_lootbox_to_inventory(trainer_profile,
                                                    legendary=True)
                    lootbox = LEGEND
                else:
                    await ctx.send("Invalid lootbox: **{}**"
                                   "".format(lootbox))
                    return
                self._save_trainer_file(self.trainer_data)
                msg = ("<@{}> gave <@{}> a **{}** lootbox"
                       "".format(admin_id,
                                 user_id,
                                 lootbox.title()))
                await ctx.send(msg)
        except Exception as e:
            error_msg = 'Failed to give user a lootbox: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def delete_trainer_lootbox(self, ctx, user_id, lootbox):
        """
        Deletes a lootbox from a user based on their ID

        @param ctx - context of the command sent
        @param user_id - user to give pokemon to
        @param lootbox - lootbox to give to the user
        """
        try:
            admin_id = ctx.message.author.id
            if admin_id in self.config_data["admin_list"]:
                if user_id in self.trainer_data:
                    trainer_profile = self.trainer_data[user_id]
                else:
                    await ctx.send("Trainer ID was not found.")
                    return
                if lootbox == "b":
                    lootbox = BRONZE
                elif lootbox == "s":
                    lootbox = SILVER
                elif lootbox == "g":
                    lootbox = GOLD
                elif lootbox == "l":
                    lootbox = LEGEND
                else:
                    await ctx.send("Invalid lootbox: **{}**"
                                   "".format(lootbox))
                    return
                if trainer_profile["lootbox"][lootbox] > 0:
                    trainer_profile["lootbox"][lootbox] -= 1
                    self._save_trainer_file(self.trainer_data)
                    msg = ("<@{}> deleted a **{}** lootbox from <@{}>"
                           "".format(admin_id,
                                     lootbox.title(),
                                     user_id))
                    await ctx.send(msg)
                else:
                    await ctx.send("The user does not have any **{}** "
                                   "lootboxes.".format(lootbox.title()))
        except Exception as e:
            error_msg = 'Failed to delete a lootbox from user: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def reload_data(self, ctx):
        """
        Reloads cog manager
        """
        try:
            admin_id = ctx.message.author.id
            if admin_id in self.config_data["admin_list"]:
                self.nrml_pokemon = self._load_pokemon_imgs()
                self.shiny_pokemon = self._load_pokemon_imgs(shiny=True)
                self.daily_data = self._load_daily_file()
                self.gift_data = self._load_gift_file()
                self.trainer_data = self._load_trainer_file()
                self.config_data = self._load_config_file()
                self.legendary_pkmn = self._load_legendary_file()
                self.ultra_beasts = self._load_ultra_file()
                self.pokeball = self._load_pokeball_file()
                self.event = PokemonEvent(self.bot, self.config_data)
                await ctx.send("Reload complete.")
        except Exception as e:
            error_msg = 'Failed to reload: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def display_ranking(self, ctx, option):
        """
        Displays the top 10 trainer rankings
        """
        try:
            if not self.trainer_cache:
                await ctx.send("Trainer data is still loading. "
                               "Please wait and try again later.")
                return
            trainer_profile = {}
            header = ''
            msg = ''
            pkmn_count = 0
            for trainer in self.trainer_data:
                pinventory = self.trainer_data[trainer]["pinventory"]
                if option == "l":
                    header = "Legendary Pokémon"
                    for pkmn in pinventory:
                        if pkmn in self.legendary_pkmn:
                            pkmn_count += pinventory[pkmn]
                elif option == "s":
                    header = "Shiny Pokémon"
                    for pkmn in pinventory:
                        if "Shiny" in pkmn:
                            pkmn_count += pinventory[pkmn]
                elif option == "t":
                    header = "Total Pokémon"
                    for pkmn in pinventory:
                        pkmn_count += pinventory[pkmn]
                elif option == "u":
                    header = "Ultra Beasts"
                    for pkmn in pinventory:
                        if pkmn in self.ultra_beasts:
                            pkmn_count += pinventory[pkmn]
                else:
                    await ctx.send("`{}` is not a valid option. The options"
                                   " are:\n"
                                   "**l** - legendary\n"
                                   "**s** - shiny\n"
                                   "**t** - total (default)\n"
                                   "**u** - ultra\n"
                                   "".format(option))
                    return
                trainer_profile[trainer] = pkmn_count
                pkmn_count = 0
            rank_num = 0
            count = 0
            for trainer in sorted(trainer_profile.items(),
                                  key=itemgetter(1),
                                  reverse=True):
                if count >= 10:
                    break
                count += 1
                rank_num += 1
                user_obj = self.trainer_cache[str(trainer[0])]
                msg += "{}. **{}** ({} caught)\n".format(rank_num,
                                                         user_obj.name,
                                                         trainer[1])
            em = discord.Embed(title="Ranking ({})".format(header),
                               description=msg,
                               colour=0xFFDF00)
            await ctx.send(embed=em)
        except Exception as e:
            error_msg = 'Failed to display ranking: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def release_pokemon(self, ctx, pkmn, quantity, save=True, post=True):
        """
        Releases a pokemon from the trainer's inventory
        """
        try:
            user_id = ctx.message.author.id
            valid_user = await self._valid_user(ctx, user_id)
            if not valid_user:
                return
            pinventory = self.trainer_data[user_id]["pinventory"]
            if pkmn not in pinventory:
                await ctx.send("Pokémon doesn't exist in the inventory"
                               " (**{}**). Please make sure there's a "
                               "valid quantity of this pokémon."
                               "".format(pkmn.title()))
                return False
            else:
                if quantity > pinventory[pkmn]:
                    await ctx.send("Can't release more than what you "
                                   "own. (Max quantity: **{}**)"
                                   "".format(pinventory[pkmn]))
                    return False
                pinventory[pkmn] -= quantity
                if pinventory[pkmn] < 1:
                    pinventory.pop(pkmn)
                if save:
                    self._save_trainer_file(self.trainer_data)
                if post:
                    await ctx.send("**{}** released **{} {}**"
                                   "".format(self.trainer_cache[user_id].name,
                                             quantity,
                                             pkmn.title()))
                await self._display_total_pokemon_caught()
                return True
        except Exception as e:
            error_msg = 'Failed to release pokemon: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def display_pinventory(self, ctx, page_number):
        """
        Displays pokemon inventory
        """
        try:
            trainer_id = str(ctx.message.author.id)
            valid_user = await self._valid_user(ctx, trainer_id)
            if not valid_user:
                return
            if page_number <= 1:
                page_number = 1
            user = ctx.message.author.name
            pinventory = self.trainer_data[trainer_id]["pinventory"]
            pinventory_count = 0
            msg = ''
            i = (page_number-1)*20
            count = 0
            for pkmn in sorted(pinventory.items()):
                if i <= count and i < 20*page_number:
                    pkmn_result = ''
                    if pkmn[0] in self.legendary_pkmn:
                        pkmn_result = "**{}** x{}\n".format(pkmn[0].title(),
                                                            pkmn[1])
                    if pkmn[0] in self.ultra_beasts:
                        pkmn_result = "**{}** x{}\n".format(pkmn[0].title(),
                                                            pkmn[1])
                    if pkmn_result == '':
                        msg += "{} x{}\n".format(pkmn[0].title(), pkmn[1])
                    else:
                        msg += pkmn_result
                    i += 1
                pinventory_count += int(pkmn[1])
                count += 1
            max_pages = ceil(len(pinventory)/20) if len(pinventory) != 0 else 1
            if page_number > max_pages:
                await ctx.send("Page number is invalid.")
                return
            msg = ("__**{}** Pokémon total. "
                   "(Page **{} of {}**)__\n"
                   "".format(pinventory_count, page_number, max_pages)
                   + msg)
            em = discord.Embed(title="{}'s Inventory".format(user),
                               description=msg,
                               colour=0xff0000)
            try:
                user_obj = await self.bot.fetch_user(ctx.message.author.id)
                await user_obj.send(embed=em)
            except:
                pass
        except Exception as e:
            print("An error has occured in displaying inventory. "
                  "See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def display_lootbox_inventory(self, ctx):
        """
        Displays pokemon inventory
        """
        try:
            user_id = str(ctx.message.author.id)
            valid_user = await self._valid_user(ctx, user_id)
            if not valid_user:
                return
            user = ctx.message.author.name
            file_changed = False
            if "lootbox" not in self.trainer_data[user_id]:
                self.trainer_data[user_id]["lootbox"] = {}
                file_changed = True
            lootbox_inv = self.trainer_data[user_id]["lootbox"]
            if BRONZE not in lootbox_inv:
                lootbox_inv["bronze"] = 0
                file_changed = True
            if SILVER not in lootbox_inv:
                lootbox_inv["silver"] = 0
                file_changed = True
            if GOLD not in lootbox_inv:
                lootbox_inv["gold"] = 0
                file_changed = True
            if LEGEND not in lootbox_inv:
                lootbox_inv["legendary"] = 0
                file_changed = True
            if file_changed:
                self._save_trainer_file(self.trainer_data)
            msg = ''
            for lootbox in lootbox_inv.items():
                msg += "**{}:** **{}**\n".format(lootbox[0].title(),
                                                 lootbox[1])
            em = discord.Embed(title="{}'s Lootboxes".format(user),
                               description=msg,
                               colour=0xFF9900)
            try:
                await ctx.send(embed=em)
            except:
                pass
        except Exception as e:
            print("An error has occured in displaying inventory. "
                  "See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def display_gif(self, ctx, pkmn_name, shiny):
        """
        Displays a gif of the pokemon

        @param pkmn_name - name of the pokemon to find a gif of
        """
        try:
            em = discord.Embed()
            if shiny == "shiny" or shiny == "s":
                em.set_image(url="https://play.pokemonshowdown.com/sprites/"
                                 "xyani-shiny/{}.gif"
                                 "".format(pkmn_name))
            else:
                em.set_image(url="https://play.pokemonshowdown.com/sprites/"
                                 "xyani/{}.gif"
                                 "".format(pkmn_name))
            await ctx.send(embed=em)
        except Exception as e:
            print("An error has occured in displaying a gif. "
                  "See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def display_trainer_profile(self, ctx, trainer):
        """
        Gets trainer profile of a trainer specified

        @param trainer - trainer to look up
        """
        try:
            user_id = re.search(r'\d+', trainer)
            user_id = str(user_id.group(0))
            valid_user = await self._valid_user(ctx, user_id)
            if not valid_user:
                return
            user_obj = self.trainer_cache[user_id]
            legendary_pkmn_count = 0
            ultra_beasts_count = 0
            shiny_pkmn_count = 0
            total_pkmn_count = 0
            if user_id in self.trainer_data:
                pinventory = self.trainer_data[user_id]["pinventory"]
                for pkmn in pinventory:
                    if pkmn in self.legendary_pkmn:
                        legendary_pkmn_count += pinventory[pkmn]
                    if pkmn in self.ultra_beasts:
                        ultra_beasts_count += pinventory[pkmn]
                    if "Shiny" in pkmn:
                        shiny_pkmn_count += pinventory[pkmn]
                    total_pkmn_count += pinventory[pkmn]
            else:
                await ctx.send("Trainer hasn't set off on his journey to "
                               "catch 'em all yet. (Catch a pokemon first in "
                               "order to use this bot command).")
                return
            em = discord.Embed()
            em.set_author(name=user_obj)
            em.set_thumbnail(url=user_obj.avatar_url)
            em.add_field(name="Legendary Pokémon caught",
                         value=legendary_pkmn_count)
            em.add_field(name="Ultra Beasts caught",
                         value=ultra_beasts_count)
            em.add_field(name="Shiny Pokémon caught︀",
                         value=shiny_pkmn_count)
            em.add_field(name="Total Pokémon caught",
                         value=total_pkmn_count)
            await ctx.send(embed=em)
        except Exception as e:
            print("An error has occured in displaying trainer profile. "
                  "See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def _load_cooldown(self, ctx, current_time):
        """
        Checks if cooldown has passed
        True if cooldown is still active
        False if cooldown is not active
        """
        user_id = ctx.message.author.id
        timer = float(self.trainer_data[user_id]["timer"])
        happy_hour_event = self.event.happy_hour_event_data
        cooldown_seconds = self.config_data["cooldown_seconds"]
        if self.event.happy_hour:
            cooldown_seconds //= happy_hour_event["cooldown_divider"]
        cooldown_limit = datetime.timedelta(seconds=cooldown_seconds)
        time_passed = datetime.timedelta(seconds=time.time()-timer)
        current_cooldown = cooldown_limit.total_seconds() - time_passed.total_seconds()
        converted_cooldown = datetime.timedelta(seconds=current_cooldown)
        if converted_cooldown.total_seconds() <= 0:
            return False
        else:
            time_left = str(converted_cooldown).split(':')
            msg = "<@{}>, you have ".format(user_id)
            if int(time_left[0]) > 0:
                msg += "**{} hour(s),** ".format(int(time_left[0]))
            msg += "**{} minutes and** ".format(int(time_left[1]))
            msg += "**{} seconds** ".format(int(float(time_left[2])))
            msg += "left before you can catch another pokémon."
            await ctx.send(msg)
            return True

    async def _post_unique_channel(self, msg, channel, pkmn, is_shiny):
        if channel is not None:
            em = discord.Embed(description=msg,
                               colour=0xFFFFFF)
            if is_shiny:
                em.set_thumbnail(url="{}{}.png".format(SHINY_ICON_URL,
                                                       pkmn.replace('_', '-')))
                em.set_image(url="{}{}.gif".format(SHINY_GIF_URL,
                                                   pkmn.replace('_', '')))
            else:
                em.set_thumbnail(url="{}{}.png".format(NRML_ICON_URL,
                                                       pkmn.replace('_', '-')))
                em.set_image(url="{}{}.gif".format(NRML_GIF_URL,
                                                   pkmn.replace('_', '')))
            try:
                await channel.send(embed=em)
            except:
                pass

    async def _post_pokemon_catch(self, ctx, random_pkmn, pkmn_img_path, random_pkmnball, is_shiny, catch_condition, lootbox):
        """
        Posts the pokemon that was caught
        """
        try:
            ctx_channel = ctx.message.channel
            user = "**{}**".format(ctx.message.author.name)
            msg = ("{} {} a {}**{}**"
                   "".format(user,
                             catch_condition,
                             random_pkmnball,
                             random_pkmn.replace('_', ' ').title()))
            msg += " and got a **{}** lootbox!".format(lootbox.title()) if lootbox is not None else "!"
            legendary = False
            special_channel = None
            if random_pkmn in self.legendary_pkmn:
                legendary = True
            try:
                if legendary or random_pkmn in self.ultra_beasts:
                    for channel in ctx.message.server.channels:
                        if "special" == channel.name:
                            special_channel = self.bot.get_channel(channel.id)
                            break
                    await self._post_unique_channel(msg,
                                                    special_channel,
                                                    random_pkmn,
                                                    is_shiny)
                if is_shiny:
                    type_pkmn = re.search(r'\-.*$', random_pkmn)
                    if type_pkmn is not None:
                        base_pkmn = random_pkmn.replace(type_pkmn[0], '')
                    else:
                        base_pkmn = random_pkmn
                    for channel in ctx.message.server.channels:
                        if "shiny" == channel.name:
                            shiny_channel = self.bot.get_channel(channel.id)
                            break
                    await self._post_unique_channel(msg,
                                                    shiny_channel,
                                                    base_pkmn,
                                                    is_shiny)
            except:
                pass
            try:
                await ctx_channel.send(file=File(pkmn_img_path),
                                       content=msg)
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print("An error has occured in posting catch. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _generate_random_pokemon(self, shiny_rate_multiplier=None):
        """
        Generates a random pokemon

        @param shiny_rate_multiplier - number to multiply the current
                                       shiny rate by
        """
        shiny_rng = random.uniform(0, 1)
        shiny_rate = self.config_data["shiny_rate"]
        if shiny_rate_multiplier is not None:
            shiny_rate *= shiny_rate_multiplier
        elif self.event.happy_hour:
            happy_hour_event = self.event.happy_hour_event_data
            shiny_rate *= happy_hour_event["shiny_rate_multiplier"]
        if shiny_rng < shiny_rate:
            random_pkmn = random.choice(list(self.shiny_pokemon.keys()))
            pkmn_img_path = self.shiny_pokemon[random_pkmn][0]
            is_shiny = True
        else:
            random_pkmn = random.choice(list(self.nrml_pokemon.keys()))
            pkmn_img_path = self.nrml_pokemon[random_pkmn][0]
            is_shiny = False
        return random_pkmn, pkmn_img_path, is_shiny

    def _move_pokemon_to_inventory(self, trainer_profile, random_pkmn, is_shiny):
        """
        Moves the pokemon to the trainer's inventory
        """
        if is_shiny:
            random_pkmn += "(Shiny)"
        if random_pkmn not in trainer_profile["pinventory"]:
            trainer_profile["pinventory"][random_pkmn] = 1
        else:
            trainer_profile["pinventory"][random_pkmn] += 1

    def _move_lootbox_to_inventory(self, trainer_profile, **kwargs):
        """
        Moves lootbox to lootbox inventory

        @param trainer_profile - trainer profile
        @param **kwargs - type of lootbox
        """
        generated_lootbox = ''
        for box in kwargs.items():
            if box[0] is BRONZE:
                generated_lootbox = BRONZE
            elif box[0] is SILVER:
                generated_lootbox = SILVER
            elif box[0] is GOLD:
                generated_lootbox = GOLD
            elif box[0] is LEGEND:
                generated_lootbox = LEGEND
        if "lootbox" not in trainer_profile:
            trainer_profile["lootbox"] = {}
        if generated_lootbox not in trainer_profile["lootbox"]:
            trainer_profile["lootbox"][generated_lootbox] = 0
        trainer_profile["lootbox"][generated_lootbox] += 1

    def _generate_lootbox(self, trainer_profile, daily=False):
        """
        Generates a lootbox depending on rng

        @param trainer_profile - trainer profile
        """
        lootbox_rng = random.uniform(0, 1)
        if daily:
            lootbox_bronze_rate = self.config_data["daily_lootbox_bronze_rate"]
            lootbox_silver_rate = self.config_data["daily_lootbox_silver_rate"]
            lootbox_gold_rate = self.config_data["daily_lootbox_gold_rate"]
            lootbox_legendary_rate = self.config_data["daily_lootbox_legendary_rate"]
        else:
            lootbox_bronze_rate = self.config_data["lootbox_bronze_rate"]
            lootbox_silver_rate = self.config_data["lootbox_silver_rate"]
            lootbox_gold_rate = self.config_data["lootbox_gold_rate"]
            lootbox_legendary_rate = self.config_data["lootbox_legendary_rate"]
        if lootbox_rng < lootbox_legendary_rate:
            self._move_lootbox_to_inventory(trainer_profile, legendary=True)
            return "legendary"
        elif lootbox_rng < lootbox_gold_rate:
            self._move_lootbox_to_inventory(trainer_profile, gold=True)
            return "gold"
        elif lootbox_rng < lootbox_silver_rate:
            self._move_lootbox_to_inventory(trainer_profile, silver=True)
            return "silver"
        elif lootbox_rng < lootbox_bronze_rate:
            self._move_lootbox_to_inventory(trainer_profile, bronze=True)
            return "bronze"
        return None

    async def catch_pokemon(self, ctx):
        """
        Generates a random pokemon to be caught
        """
        try:
            current_time = time.time()
            user_id = ctx.message.author.id
            if user_id not in self.trainer_data:
                user_obj = await self.bot.fetch_user(user_id)
                self.trainer_data[user_id] = {}
                self.trainer_data[user_id]["pinventory"] = {}
                self.trainer_data[user_id]["timer"] = False
                self.trainer_cache[user_id] = user_obj
            if not await self._load_cooldown(ctx, current_time):
                random_pkmn, pkmn_img_path, is_shiny = self._generate_random_pokemon()
                random_pkmnball = random.choice(list(self.pokeball))
                trainer_profile = self.trainer_data[user_id]
                trainer_profile["timer"] = current_time
                lootbox = self._generate_lootbox(trainer_profile)
                self._move_pokemon_to_inventory(trainer_profile,
                                                random_pkmn,
                                                is_shiny)
                self._save_trainer_file(self.trainer_data)
                await self._display_total_pokemon_caught()
                await self._post_pokemon_catch(ctx,
                                               random_pkmn,
                                               pkmn_img_path,
                                               random_pkmnball,
                                               is_shiny,
                                               "caught",
                                               lootbox)
        except Exception as e:
            print("An error has occured in catching pokemon. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def _check_hatched_pokemon(self, pinventory, pkmn):
        """
        Checks if the hatched pokemon is valid

        @param pinventory - the trainer's pokemon inventory
        @param pkmn - pkmn to check
        @return - True if pkmn is not a legendary/ultra beast
                  False if pkmn is a legendary/ultra beast
        """
        egg = "egg"
        egg_manaphy = "egg-manaphy"
        if pkmn in self.legendary_pkmn:
            return False
        if pkmn in self.ultra_beasts:
            return False
        if egg == pkmn:
            return False
        if egg_manaphy == pkmn:
            return False
        return True

    async def hatch_egg(self, ctx):
        """
        Hatches an egg from the trainer's inventory

        @param ctx - context of the command
        @param egg - egg to hatch
        """
        try:
            egg = "egg"
            egg_manaphy = "egg-manaphy"
            user_id = str(ctx.message.author.id)
            valid_user = await self._valid_user(ctx, user_id)
            if not valid_user:
                return
            pinventory = self.trainer_data[user_id]["pinventory"]
            if egg in pinventory:
                shiny_rng = random.uniform(0, 1)
                if shiny_rng < self.config_data["shiny_rate"]*self.config_data["shiny_hatch_multiplier"]:
                    random_pkmn = random.choice(list(self.shiny_pokemon.keys()))
                    valid_pkmn = await self._check_hatched_pokemon(pinventory,
                                                                   random_pkmn)
                    while not valid_pkmn:
                        random_pkmn = random.choice(list(self.shiny_pokemon.keys()))
                        valid_pkmn = await self._check_hatched_pokemon(pinventory,
                                                                       random_pkmn)
                    pkmn_img_path = self.shiny_pokemon[random_pkmn][0]
                    is_shiny = True
                else:
                    random_pkmn = random.choice(list(self.nrml_pokemon.keys()))
                    valid_pkmn = await self._check_hatched_pokemon(pinventory,
                                                                   random_pkmn)
                    while not valid_pkmn:
                        random_pkmn = random.choice(list(self.nrml_pokemon.keys()))
                        valid_pkmn = await self._check_hatched_pokemon(pinventory,
                                                                       random_pkmn)
                    pkmn_img_path = self.nrml_pokemon[random_pkmn][0]
                    is_shiny = False
                pinventory[egg] -= 1
                if pinventory[egg] < 1:
                    pinventory.pop(egg)
            elif egg_manaphy in pinventory:
                shiny_rng = random.uniform(0, 1)
                random_pkmn = "manaphy"
                if shiny_rng < self.config_data["shiny_rate"]*self.config_data["shiny_hatch_multiplier"]:
                    pkmn_img_path = self.shiny_pokemon[random_pkmn][0]
                    is_shiny = True
                else:
                    pkmn_img_path = self.nrml_pokemon[random_pkmn][0]
                    is_shiny = False
                pinventory[egg_manaphy] -= 1
                if pinventory[egg_manaphy] < 1:
                    pinventory.pop(egg_manaphy)
            else:
                await ctx.send("There are no eggs in the trainer's inventory.")
                return
            self._move_pokemon_to_inventory(self.trainer_data[user_id],
                                            random_pkmn,
                                            is_shiny)
            self._save_trainer_file(self.trainer_data)
            random_pkmnball = random.choice(list(self.pokeball))
            await self._post_pokemon_catch(ctx,
                                           random_pkmn,
                                           pkmn_img_path,
                                           random_pkmnball,
                                           is_shiny,
                                           "hatched",
                                           None)
        except Exception as e:
            print("An error has occured in hatching egg. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def fuse_pokemon(self, ctx, pkmn, form_list):
        """
        Retrieves all type-specific forms of a pokemon and fuses them to
        get the original

        @param ctx - context of the command
        @param pkmn - pokemon to fuse into
        @param form_list - 5 pokemon to fuse to get to the original
        """
        try:
            msg = ''
            user_id = str(ctx.message.author.id)
            valid_user = await self._valid_user(ctx, user_id)
            if not valid_user:
                return
            if pkmn in self.nrml_pokemon.keys():
                regex_pkmn = pkmn+'-'
                pkmn_forms = [p for p in self.nrml_pokemon.keys() if regex_pkmn in p]
                if not pkmn_forms or len(pkmn_forms) == 1:
                    await ctx.send("There are no multiple forms to fuse "
                                   "for this pokemon.")
                    return
                elif form_list and len(pkmn_forms) < 5:
                    await ctx.send("You must have all forms to fuse this "
                                   "pokemon.")
                    return
                trainer_profile = self.trainer_data[user_id]
                if len(form_list) == 0:
                    if len(pkmn_forms) >= 5:
                        await ctx.send("This pokemon has many forms. "
                                       "Use the command again but also "
                                       "specify 5 forms of this pokemon you "
                                       "would like to use for this fusion.")
                        return
                    for p in pkmn_forms:
                        if p not in trainer_profile["pinventory"]:
                            msg += "**{}**\n".format(p.title())
                    if msg != '':
                        await ctx.send("**{}** is missing the following "
                                       "forms to fuse:\n{}"
                                       "".format(ctx.message.author.name,
                                                 msg))
                        return
                if len(form_list) != 5:
                    await ctx.send("Invalid number of pokemon forms "
                                   "inputted. Please "
                                   "enter 5 pokemon forms from your "
                                   "inventory you wish to use.")
                    return
                release_list = pkmn_forms if form_list is None else form_list
                for p in release_list:
                    if p in pkmn_forms:
                        successful = await self.release_pokemon(ctx,
                                                                p,
                                                                1,
                                                                False,
                                                                False)
                        if not successful:
                            self.trainer_data = self._load_trainer_file()
                            return
                    else:
                        await ctx.send("**{}** is not a valid pokemon to "
                                       "use for this fusion."
                                       "".format(p.title()))
                        self.trainer_data = self._load_trainer_file()
                        return
                self._move_pokemon_to_inventory(trainer_profile,
                                                pkmn,
                                                False)
                self._save_trainer_file(self.trainer_data)
                random_pkmnball = random.choice(list(self.pokeball))
                await self._post_pokemon_catch(ctx,
                                               pkmn,
                                               self.nrml_pokemon[pkmn][0],
                                               random_pkmnball,
                                               False,
                                               "fused for",
                                               None)
            else:
                await ctx.send("Not a valid pokemon: **{}**"
                               "".format(pkmn.title()))
        except Exception as e:
            print("An error has occured in fusing pokemon. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def exchange_pokemon(self, ctx, pokemon_list):
        """
        Exchanges 5 pokemon for 1 with a 5x shiny chance

        @param ctx - context of the command
        @param pokemon_list - 5 pokemon to exchange
        """
        try:
            user_id = str(ctx.message.author.id)
            valid_user = await self._valid_user(ctx, user_id)
            if not valid_user:
                return
            if len(pokemon_list) != 5:
                await ctx.send("Please enter only 5 pokemon to exchange.")
                return
            for pkmn in pokemon_list:
                successful = await self.release_pokemon(ctx,
                                                        pkmn,
                                                        1,
                                                        False,
                                                        False)
                if not successful:
                    self.trainer_data = self._load_trainer_file()
                    return
            shiny_exchange_multiplier = self.config_data["shiny_exchange_multiplier"]
            random_pkmn, pkmn_img_path, is_shiny = self._generate_random_pokemon(shiny_exchange_multiplier)
            random_pkmnball = random.choice(list(self.pokeball))
            trainer_profile = self.trainer_data[user_id]
            self._move_pokemon_to_inventory(trainer_profile,
                                            random_pkmn,
                                            is_shiny)
            self._save_trainer_file(self.trainer_data)
            await self._post_pokemon_catch(ctx,
                                           random_pkmn,
                                           pkmn_img_path,
                                           random_pkmnball,
                                           is_shiny,
                                           "exchanged for",
                                           None)
        except Exception as e:
            print("Failed to exchange pokemon. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def _generate_lootbox_pokemon(self, ctx, lootbox):
        """
        Generates pokemon from the lootbox opened and displays what you got
        """
        user_id = ctx.message.author.id
        lootbox_pokemon_limit = self.config_data["lootbox_pokemon_limit"]
        shiny_lootbox_multiplier = self.config_data["shiny_lootbox_multiplier"]
        trainer_profile = self.trainer_data[user_id]
        pokemon_obtained = {}
        i = 0
        lootbox_color = ''
        if lootbox == BRONZE:
            while i < lootbox_pokemon_limit:
                pkmn = self._generate_random_pokemon(shiny_lootbox_multiplier)
                is_shiny = pkmn[2]
                pkmn = pkmn[0]
                while (pkmn in self.legendary_pkmn or pkmn in self.ultra_beasts
                       or pkmn in pokemon_obtained):
                    pkmn = self._generate_random_pokemon(shiny_lootbox_multiplier)
                    is_shiny = pkmn[2]
                    pkmn = pkmn[0]
                pokemon_obtained[pkmn] = is_shiny
                i += 1
            thumbnail_url = ("https://github.com/msikma/pokesprite/blob/master/"
                             "icons/pokeball/poke.png?raw=true")
            lootbox_color = 0xCD7F32
        elif lootbox == SILVER:
            while i < lootbox_pokemon_limit:
                pkmn = self._generate_random_pokemon(shiny_lootbox_multiplier)
                is_shiny = pkmn[2]
                pkmn = pkmn[0]
                while pkmn in self.ultra_beasts or pkmn in pokemon_obtained:
                    pkmn = self._generate_random_pokemon(shiny_lootbox_multiplier)
                    is_shiny = pkmn[2]
                    pkmn = pkmn[0]
                pokemon_obtained[pkmn] = is_shiny
                i += 1
            thumbnail_url = ("https://github.com/msikma/pokesprite/blob/master/"
                             "icons/pokeball/great.png?raw=true")
            lootbox_color = 0xC0C0C0
        elif lootbox == GOLD:
            while i < lootbox_pokemon_limit:
                pkmn = self._generate_random_pokemon(shiny_lootbox_multiplier)
                is_shiny = pkmn[2]
                pkmn = pkmn[0]
                while pkmn in pokemon_obtained:
                    pkmn = self._generate_random_pokemon(shiny_lootbox_multiplier)
                    is_shiny = pkmn[2]
                    pkmn = pkmn[0]
                pokemon_obtained[pkmn] = is_shiny
                i += 1
            thumbnail_url = ("https://github.com/msikma/pokesprite/blob/master/"
                             "icons/pokeball/ultra.png?raw=true")
            lootbox_color = 0xFFDF00
        elif lootbox == LEGEND:
            while i < lootbox_pokemon_limit:
                pkmn = self._generate_random_pokemon(shiny_lootbox_multiplier)
                is_shiny = pkmn[2]
                pkmn = pkmn[0]
                while (pkmn not in self.legendary_pkmn and pkmn not in self.ultra_beasts
                       or pkmn in pokemon_obtained):
                    pkmn = self._generate_random_pokemon(shiny_lootbox_multiplier)
                    is_shiny = pkmn[2]
                    pkmn = pkmn[0]
                pokemon_obtained[pkmn] = is_shiny
                i += 1
            thumbnail_url = ("https://github.com/msikma/pokesprite/blob/master/"
                             "icons/pokeball/master.png?raw=true")
            lootbox_color = 0xFF9900
        else:
            await ctx.send("Lootbox failed to open: {}".format(lootbox))
            return False
        msg = ("**{}** opened the **{}** lootbox and obtained:\n"
               "".format(ctx.message.author.name, lootbox.title()))
        for pkmn in pokemon_obtained.items():
            self._move_pokemon_to_inventory(trainer_profile,
                                            pkmn[0],
                                            pkmn[1])
            if pkmn[1]:
                msg += "**{}(Shiny)**\n".format(pkmn[0].title())
            else:
                msg += "**{}**\n".format(pkmn[0].title())
        em = discord.Embed(title="Lootbox",
                           description=msg,
                           colour=lootbox_color)
        em.set_thumbnail(url=thumbnail_url)
        await ctx.send(embed=em)
        return True

    async def open_lootbox(self, ctx, lootbox):
        """
        Opens a lootbox from the trainer's inventory based on
        the trainer's specified choice

        @param lootbox - lootbox to open
        """
        try:
            if lootbox == 'b':
                lootbox = BRONZE
            elif lootbox == 's':
                lootbox = SILVER
            elif lootbox == 'g':
                lootbox = GOLD
            elif lootbox == 'l':
                lootbox = LEGEND
            user_id = str(ctx.message.author.id)
            valid_user = await self._valid_user(ctx, user_id)
            if not valid_user:
                return
            trainer_profile = self.trainer_data[user_id]
            if "lootbox" in trainer_profile:
                if lootbox in trainer_profile["lootbox"]:
                    if trainer_profile["lootbox"][lootbox] > 0:
                        success = await self._generate_lootbox_pokemon(ctx,
                                                                       lootbox)
                        if success:
                            trainer_profile["lootbox"][lootbox] -= 1
                            self._save_trainer_file(self.trainer_data)
                    else:
                        await ctx.send("<@{}> you don't have any {} "
                                       "lootboxes.".format(user_id,
                                                           lootbox))
                else:
                    await ctx.send("Lootbox does not exist or has not "
                                   "been obtained yet.")
            else:
                await ctx.send("Trainer does not have a lootbox.")
        except Exception as e:
            print("Failed to open a lootbox. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _vendor_roll(self, ctx):
        """
        Rolls the trade that the vendor wants to make
        """
        i = 0
        egg = "egg"
        egg_manaphy = "egg-manaphy"
        user_id = ctx.message.author.id
        night_vendor_event = self.event.night_vendor_event_data
        if user_id not in self.vendor_sales:
            shiny_rate_multiplier = night_vendor_event["shiny_rate_multiplier"]
            random_pkmn, pkmn_img_path, is_shiny = self._generate_random_pokemon(shiny_rate_multiplier)
            while (egg in random_pkmn or egg_manaphy in random_pkmn
                   or "-" in random_pkmn):
                random_pkmn, pkmn_img_path, is_shiny = self._generate_random_pokemon(shiny_rate_multiplier)
            self.vendor_sales[user_id] = {}
            self.vendor_sales[user_id]["pkmn"] = random_pkmn
            self.vendor_sales[user_id]["pkmn_img_path"] = pkmn_img_path
            self.vendor_sales[user_id]["shiny"] = is_shiny
        if not self.vendor_trade_list[user_id]:
            num_pkmn_to_trade = night_vendor_event["num_pkmn_to_trade"]
            while i < num_pkmn_to_trade:
                t_pkmn = self._generate_random_pokemon(0)[0]
                while (egg in t_pkmn or egg_manaphy in t_pkmn
                       or "-" in t_pkmn):
                    t_pkmn = self._generate_random_pokemon(0)[0]
                self.vendor_trade_list[user_id].append(t_pkmn)
                i += 1

    async def _vendor_info(self, ctx):
        """
        Displays info on what the vendor wants to trade
        """
        t_pkmn_list = ''
        user_id = ctx.message.author.id
        for t_pkmn in self.vendor_trade_list[user_id]:
            t_pkmn_list += '{}\n'.format(t_pkmn.title())
        pkmn = self.vendor_sales[user_id]["pkmn"]
        if self.vendor_sales[user_id]["shiny"]:
            pkmn += "(Shiny)"
        await ctx.send("The **Night Vendor** wants to trade "
                       "**{}** a **{}** for **all** of the following "
                       "pokemon:\n**{}**"
                       "".format(ctx.message.author.name,
                                 pkmn.title(),
                                 t_pkmn_list))

    async def _vendor_reroll(self, ctx):
        """
        Rerolls the vendor's trade for the user of interest
        """
        user_id = ctx.message.author.id
        trainer_profile = self.trainer_data[user_id]
        if trainer_profile["reroll_count"] > 0:
            if user_id in self.vendor_sales:
                self.vendor_sales.pop(user_id)
            if user_id in self.vendor_trade_list:
                self.vendor_trade_list.pop(user_id)
            t_pkmn_list = ''
            self._vendor_roll(ctx)
            trainer_profile["reroll_count"] -= 1
            self._save_trainer_file(self.trainer_data)
            pkmn = self.vendor_sales[user_id]["pkmn"]
            for t_pkmn in self.vendor_trade_list[user_id]:
                t_pkmn_list += '**{}**\n'.format(t_pkmn.title())
            if self.vendor_sales[user_id]["shiny"]:
                pkmn += "(Shiny)"
            await ctx.send("**{}** has re-rolled the vendor's trade (**{}**"
                           " re-rolls remaining). The **Night Vendor** "
                           "wants to trade **{}** for **all** of the "
                           "following pokemon:\n{}"
                           "".format(ctx.message.author.name,
                                     trainer_profile["reroll_count"],
                                     pkmn.title(),
                                     t_pkmn_list))
        else:
            await ctx.send("<@{}>, you don't have anymore rolls."
                           "".format(user_id))

    async def _vendor_trade(self, ctx):
        """
        Trades the vendor
        """
        msg = ''
        user_id = ctx.message.author.id
        trainer_profile = self.trainer_data[user_id]
        trade_verified = True
        for p in self.vendor_trade_list[user_id]:
            if p not in trainer_profile["pinventory"]:
                msg += "**{}**\n".format(p.title())
                trade_verified = False
        if trade_verified:
            for pkmn in self.vendor_trade_list[user_id]:
                successful = await self.release_pokemon(ctx,
                                                        pkmn,
                                                        1,
                                                        False,
                                                        False)
                if not successful:
                    self.trainer_data = self._load_trainer_file()
                    return
            vendor_pkmn_sale = self.vendor_sales[user_id]["pkmn"]
            pkmn_img_path = self.vendor_sales[user_id]["pkmn_img_path"]
            is_shiny = self.vendor_sales[user_id]["shiny"]
            self._move_pokemon_to_inventory(trainer_profile,
                                            vendor_pkmn_sale,
                                            is_shiny)
            self.vendor_sales.pop(user_id)
            self.vendor_trade_list.pop(user_id)
            random_pokeball = random.choice(list(self.pokeball))
            await self._post_pokemon_catch(ctx,
                                           vendor_pkmn_sale,
                                           pkmn_img_path,
                                           random_pokeball,
                                           is_shiny,
                                           "has traded the night vendor for",
                                           None)
            trainer_profile["reroll_count"] = 0
            self._save_trainer_file(self.trainer_data)
        else:
            await ctx.send("Unable to trade. The following Pokémon are "
                           "missing:\n{}".format(msg))

    async def vendor_options(self, ctx, option):
        """
        Carries out vendor operations depending on the option

        @param ctx - context of the command
        @param option - option the user input
        """
        try:
            if self.event.night_vendor:
                user_id = str(ctx.message.author.id)
                valid_user = await self._valid_user(ctx, user_id)
                if not valid_user:
                    return
                trainer_profile = self.trainer_data[user_id]
                if (trainer_profile["reroll_count"] > 0
                   or user_id in self.vendor_sales):
                    if user_id not in self.vendor_sales:
                        self._vendor_roll(ctx)
                    if option == "i":
                        await self._vendor_info(ctx)
                    elif option == "r":
                        await self._vendor_reroll(ctx)
                    elif option == "t":
                        await self._vendor_trade(ctx)
                    else:
                        await ctx.send("`{}` is not a valid choice"
                                       "".format(option))
                else:
                    await ctx.send("<@{}>, the night vendor is done "
                                   "doing business with you for the "
                                   "evening.".format(user_id))
            else:
                await ctx.send("The night vendor is not here.")
        except Exception as e:
            print("Failed to speak with vendor. See error.log")
            logger.error("Exception: {}".format(str(e)))

    async def claim_daily(self, ctx):
        """
        Claims the daily lootbox
        """
        try:
            user_id = ctx.message.author.id
            username = ctx.message.author.name
            if user_id not in self.trainer_data:
                user_obj = await self.bot.fetch_user(user_id)
                self.trainer_data[user_id] = {}
                self.trainer_data[user_id]["pinventory"] = {}
                self.trainer_data[user_id]["timer"] = False
                self.trainer_cache[user_id] = user_obj
            trainer_profile = self.trainer_data[user_id]
            if "lootbox" not in trainer_profile:
                trainer_profile["lootbox"] = {}
            if BRONZE not in trainer_profile["lootbox"]:
                trainer_profile["lootbox"][BRONZE] = 0
            if SILVER not in trainer_profile["lootbox"]:
                trainer_profile["lootbox"][SILVER] = 0
            if GOLD not in trainer_profile["lootbox"]:
                trainer_profile["lootbox"][GOLD] = 0
            if LEGEND not in trainer_profile["lootbox"]:
                trainer_profile["lootbox"][LEGEND] = 0
            if "daily_tokens" not in trainer_profile:
                trainer_profile["daily_tokens"] = 0
                self._save_trainer_file(self.trainer_data)
            if user_id not in self.daily_data:
                lootbox = self._generate_lootbox(trainer_profile, daily=True)
                trainer_profile["daily_tokens"] += 1
                self.daily_data.append(user_id)
                self._save_trainer_file(self.trainer_data)
                self._save_daily_file(self.daily_data)
                await ctx.send("**{}** claimed their daily to get a **{}**"
                               " lootbox as well as a daily token."
                               "".format(username,
                                         lootbox.title()))
            else:
                await ctx.send("**{}** has already claimed their daily "
                               "lootbox".format(username))
        except Exception as e:
            self.daily_data = self._load_daily_file()
            print("Failed to claim daily. See error.log")
            logger.error("Exception: {}".format(str(e)))

    async def claim_gift(self, ctx):
        """
        Claims the available gift
        """
        try:
            user_id = ctx.message.author.id
            username = ctx.message.author.name
            pkmn_msg = ''
            lootbox_msg = ''
            if user_id not in self.trainer_data:
                user_obj = await self.bot.fetch_user(user_id)
                self.trainer_data[user_id] = {}
                self.trainer_data[user_id]["pinventory"] = {}
                self.trainer_data[user_id]["timer"] = False
                self.trainer_cache[user_id] = user_obj
            trainer_profile = self.trainer_data[user_id]
            if "lootbox" not in trainer_profile:
                trainer_profile["lootbox"] = {}
            if BRONZE not in trainer_profile["lootbox"]:
                trainer_profile["lootbox"][BRONZE] = 0
            if SILVER not in trainer_profile["lootbox"]:
                trainer_profile["lootbox"][SILVER] = 0
            if GOLD not in trainer_profile["lootbox"]:
                trainer_profile["lootbox"][GOLD] = 0
            if LEGEND not in trainer_profile["lootbox"]:
                trainer_profile["lootbox"][LEGEND] = 0
            pinventory = trainer_profile["pinventory"]
            if not self.config_data["gift"]:
                await ctx.send("No gift to claim.")
                return
            if user_id not in self.gift_data:
                pokemon_list = self.config_data["gift_list"]["pokemon"]
                lootbox_list = self.config_data["gift_list"]["lootbox"]
                for pkmn in pokemon_list:
                    if pkmn not in pinventory:
                        pinventory[pkmn] = pokemon_list[pkmn]
                    else:
                        pinventory[pkmn] += pokemon_list[pkmn]
                    pkmn_msg += "**{}** x{}\n".format(pkmn.title(),
                                                      pokemon_list[pkmn])
                for lootbox in lootbox_list:
                    trainer_profile["lootbox"][lootbox] += lootbox_list[lootbox]
                    lootbox_msg += "**{}** x{}\n".format(lootbox.title(),
                                                         lootbox_list[lootbox])
                self.gift_data.append(user_id)
                self._save_trainer_file(self.trainer_data)
                self._save_gift_file(self.gift_data)
                em = discord.Embed(title="{}'s Gift\n"
                                         "".format(username),
                                   colour=0xFFFFFF)
                if pokemon_list:
                    em.add_field(name="Pokemon",
                                 value=pkmn_msg)
                if lootbox_list:
                    em.add_field(name="Lootbox",
                                 value=lootbox_msg)
                await ctx.send(embed=em)
            else:
                await ctx.send("<@{}>, you've already claimed your "
                               "gift".format(user_id))
        except Exception as e:
            self.gift_data = self._load_gift_file()
            print("Failed to claim gift. See error.log")
            logger.error("Exception: {}".format(str(e)))

    async def display_daily_tokens(self, ctx):
        """
        Displays the player's daily token
        """
        try:
            user_id = ctx.message.author.id
            if user_id not in self.trainer_data:
                await ctx.send("Please catch a pokemon with `p.c` first.")
            trainer_profile = self.trainer_data[user_id]
            if "daily_tokens" not in trainer_profile:
                trainer_profile["daily_tokens"] = 0
                self._save_trainer_file(self.trainer_data)
            await ctx.send("<@{}> currently has **{}** daily tokens."
                           "".format(user_id,
                                     trainer_profile["daily_tokens"]))
        except Exception as e:
            print("Failed to display daily tokens.")
            logger.error("Exception: {}".format(str(e)))

    async def daily_shop(self, ctx, option, item_num):
        """
        Displays the daily shop via options
        """
        try:
            user_id = ctx.message.author.id
            trainer_profile = self.trainer_data[user_id]
            if user_id not in self.trainer_data:
                await ctx.send("Please catch a pokemon with `p.c` first.")
                return
            if option == "i":
                menu_items = ("[1] - Bronze lootbox (**{}** tokens)\n"
                              "[2] - Silver lootbox (**{}** tokens)\n"
                              "[3] - Gold lootbox (**{}** tokens)\n"
                              "[4] - Legendary lootbox (**{}** tokens)\n"
                              "[5] - Random shiny pokemon (**{}** tokens)\n"
                              "".format(BRONZE_LOOTBOX_PRICE,
                                        SILVER_LOOTBOX_PRICE,
                                        GOLD_LOOTBOX_PRICE,
                                        LEGENDARY_LOOTBOX_PRICE,
                                        RANDOM_SHINY_PRICE))
                em = discord.Embed(title="Daily Token Shop",
                                   description=menu_items)
                await ctx.send(embed=em)
            elif option == "b":
                if item_num is None:
                    await ctx.send("Please enter the item number you wish to buy.")
                    return
                token_num = int(trainer_profile["daily_tokens"])
                if item_num == '1':
                    if token_num < BRONZE_LOOTBOX_PRICE:
                        await ctx.send("<@{}>, you do not have enough tokens."
                                       "".format(user_id))
                        return
                    trainer_profile["daily_tokens"] = token_num - BRONZE_LOOTBOX_PRICE
                    trainer_profile["lootbox"][BRONZE] += 1
                    await ctx.send("<@{}> bought a **Bronze** lootbox.".format(user_id))
                elif item_num == '2':
                    if token_num < SILVER_LOOTBOX_PRICE:
                        await ctx.send("<@{}>, you do not have enough tokens."
                                       "".format(user_id))
                        return
                    trainer_profile["daily_tokens"] = token_num - SILVER_LOOTBOX_PRICE
                    trainer_profile["lootbox"][SILVER] += 1
                    await ctx.send("<@{}> bought a **Silver** lootbox.".format(user_id))
                elif item_num == '3':
                    if token_num < GOLD_LOOTBOX_PRICE:
                        await ctx.send("<@{}>, you do not have enough tokens."
                                       "".format(user_id))
                        return
                    trainer_profile["daily_tokens"] = token_num - GOLD_LOOTBOX_PRICE
                    trainer_profile["lootbox"][SILVER] += 1
                    await ctx.send("<@{}> bought a **Gold** lootbox.".format(user_id))
                elif item_num == '4':
                    if token_num < LEGENDARY_LOOTBOX_PRICE:
                        await ctx.send("<@{}>, you do not have enough tokens."
                                       "".format(user_id))
                        return
                    trainer_profile["daily_tokens"] = token_num - LEGENDARY_LOOTBOX_PRICE
                    trainer_profile["lootbox"][LEGEND] += 1
                    await ctx.send("<@{}> bought a **Legendary** lootbox.".format(user_id))
                elif item_num == '5':
                    if token_num < RANDOM_SHINY_PRICE:
                        await ctx.send("<@{}>, you do not have enough tokens."
                                       "".format(user_id))
                        return
                    trainer_profile["daily_tokens"] = token_num - RANDOM_SHINY_PRICE
                    pkmn = self._generate_random_pokemon(50000)
                    random_pkmnball = random.choice(list(self.pokeball))
                    self._move_pokemon_to_inventory(trainer_profile,
                                                    pkmn[0],
                                                    pkmn[2])
                    await self._post_pokemon_catch(ctx,
                                                   pkmn[0],
                                                   pkmn[1],
                                                   random_pkmnball,
                                                   pkmn[2],
                                                   "bought",
                                                   None)
                else:
                    await ctx.send("Invalid choice. Please enter a number from the "
                                   "daily shop")
                    return
                self._save_trainer_file(self.trainer_data)
            else:
                await ctx.send("Please enter a valid option.")
        except Exception as e:
            print("Failed to perform shop operations.")
            logger.error("Exception: {}".format(str(e)))
