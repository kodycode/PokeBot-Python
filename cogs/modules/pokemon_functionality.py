from bot_logger import logger
from cogs.modules.pokemon_event import PokemonEvent
from collections import defaultdict
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


class PokemonFunctionality:
    """Handles Pokemon Command Functionality"""

    def __init__(self, bot):
        self.bot = bot
        self.trainer_cache = {}
        self.config_data = self._check_config_file()
        self.legendary_pkmn = self._check_legendary_file()
        self.ultra_pkmn = self._check_ultra_file()
        self.pokeball = self._check_pokeball_file()
        self.cooldown_seconds = self.config_data["cooldown_seconds"]
        self.shiny_rate = self.config_data["shiny_rate"]
        self.shiny_hatch_multiplier = self.config_data["shiny_hatch_multiplier"]
        self.event = PokemonEvent(bot)
        self.nrml_pokemon = self._load_pokemon_imgs()
        self.shiny_pokemon = self._load_pokemon_imgs(shiny=True)
        self.trainer_data = self._check_trainer_file()
        self._save_trainer_file(self.trainer_data, backup=True)
        self.bot.loop.create_task(self._update_cache())
        self.bot.loop.create_task(self._display_total_pokemon_caught())
        self.bot.loop.create_task(self._check_event())

    async def update_game_status(self, total_pkmn_count):
        """
        Updates the game status of the bot
        """
        try:
            game_status = discord.Game(name="{} Pokémon caught"
                                            "".format(total_pkmn_count))
            await self.bot.change_presence(game=game_status)
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
                user_obj = await self.bot.get_user_info(str(trainer))
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

    async def _check_event(self):
        """
        Checks if it's time for an event
        """
        while True:
            hour = int(datetime.datetime.now().hour)
            happy_hour_event = self.event.event_data["happy_hour_event"]
            if happy_hour_event["event"]:
                if hour == happy_hour_event["event_start_hour"]:
                    await self.event.activate_happy_hour()
                    await asyncio.sleep(happy_hour_event["duration"])
                    await self.event.deactivate_happy_hour()
            await asyncio.sleep(60)

    def _check_config_file(self):
        """
        Checks to see if there's a valid config.json file
        """
        try:
            with open('config.json') as config:
                return json.load(config)
        except FileNotFoundError:
            msg = "FileNotFoundError: 'config.json' file not found"
            print(msg)
            logger.error(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _check_legendary_file(self):
        """
        Checks to see if there's a valid legendary_pkmn.json file
        """
        try:
            with open('legendary_pkmn.json') as legendaries:
                return json.load(legendaries)
        except FileNotFoundError:
            msg = "FileNotFoundError: 'legendary_pkmn.json' file not found"
            print(msg)
            logger.error(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _check_ultra_file(self):
        """
        Checks to see if there's a valid ultra_pkmn.json file
        """
        try:
            with open('ultra_pkmn.json') as ultras:
                return json.load(ultras)
        except FileNotFoundError:
            msg = "FileNotFoundError: 'ultra_pkmn.json' file not found"
            print(msg)
            logger.error(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _check_pokeball_file(self):
        """
        Checks to see if there's a valid pokeballs.json file
        """
        try:
            with open('pokeballs.json') as pokeballs:
                return json.load(pokeballs)
        except FileNotFoundError:
            msg = "FileNotFoundError: 'pokeballs.json' file not found"
            print(msg)
            logger.error(msg)
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _check_trainer_file(self):
        """
        Checks to see if there's a valid trainers.json file
        """
        try:
            with open('trainers.json') as trainers:
                return json.load(trainers)
        except FileNotFoundError:
            self._save_trainer_file()
            return json.loads('{}')
        except Exception as e:
            print("An error has occured. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    def _save_trainer_file(self, trainer_data={}, backup=False):
        """
        Saves trainers.json file
        """
        if backup:
            trainer_filename = "trainers_backup.json"
        else:
            trainer_filename = "trainers.json"
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
                pkmn_name = filename
                pkmn_name = pkmn_name.replace(folder_path, "")
                pkmn_name = pkmn_name.replace('/', "")
                pkmn_name = pkmn_name.replace('\\', "")
                pkmn_name = pkmn_name.replace('.png', "")
                filedict[pkmn_name].append(filename)
        return filedict

    async def reload_data(self):
        """
        Reloads cog manager
        """
        try:
            self.nrml_pokemon = self._load_pokemon_imgs()
            self.shiny_pokemon = self._load_pokemon_imgs(shiny=True)
            self.trainer_data = self._check_trainer_file()
            self.config_data = self._check_config_file()
            self.cooldown_seconds = self.config_data["cooldown_seconds"]
            self.shiny_rate = self.config_data["shiny_rate"]
            self.shiny_hatch_multiplier = self.config_data["shiny_hatch_multiplier"]
            self.legendary_pkmn = self._check_legendary_file()
            self.ultra_pkmn = self._check_ultra_file()
            self.pokeball = self._check_pokeball_file()
            self.event.event_data = self.event.check_event_file()
            await self.bot.say("Reload complete.")
        except Exception as e:
            error_msg = 'Failed to reload: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def display_ranking(self, option):
        """
        Displays the top 10 trainer rankings
        """
        try:
            if not self.trainer_cache:
                await self.bot.say("Trainer data is still loading. "
                                   "Please wait and try again later.")
                return
            trainer_profile = {}
            header = ''
            msg = ''
            legendary_count = 0
            for trainer in self.trainer_data:
                pinventory = self.trainer_data[trainer]["pinventory"]
                if option == "l":
                    header = "Legendary Pokémon"
                    for pkmn in pinventory:
                        for legendary in self.legendary_pkmn:
                            if legendary in pkmn:
                                legendary_count += pinventory[pkmn]
                    trainer_profile[trainer] = legendary_count
                    legendary_count = 0
                elif option == "s":
                    header = "Shiny Pokémon"
                    for pkmn in pinventory:
                        if "Shiny" in pkmn:
                            trainer_profile[trainer] = pinventory[pkmn]
                elif option == "t":
                    header = "Total Pokémon"
                    trainer_profile[trainer] = len(pinventory)
                elif option == "u":
                    header = "Ultra Pokémon"
                    for pkmn in pinventory:
                        if pkmn in self.ultra_pkmn:
                            trainer_profile[trainer] = pinventory[pkmn]
                else:
                    await self.bot.say("`{}` is not a valid option. The options"
                                       " are:\n"
                                       "**l** - legendary\n"
                                       "**s** - shiny\n"
                                       "**t** - total (default)\n"
                                       "**u** - ultra\n"
                                       "".format(option))
                    return
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
            await self.bot.say(embed=em)
        except Exception as e:
            error_msg = 'Failed to display ranking: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def release_pokemon(self, ctx, pkmn, quantity):
        """
        Releases a pokemon from the trainer's inventory
        """
        try:
            if not self.trainer_cache:
                await self.bot.say("Trainer data is still loading. "
                                   "Please wait and try again later.")
                return
            user_id = ctx.message.author.id
            if user_id not in self.trainer_data:
                await self.bot.say("Trainer hasn't set off on his journey to "
                                   "catch 'em all yet.")
            else:
                pinventory = self.trainer_data[user_id]["pinventory"]
                if pkmn not in pinventory:
                    await self.bot.say("Pokémon doesn't exist in the inventory")
                else:
                    pinventory[pkmn] -= quantity
                    if pinventory[pkmn] < 1:
                        pinventory.pop(pkmn)
                    self._save_trainer_file(self.trainer_data)
                    await self.bot.say("**{}** released **{} {}**"
                                       "".format(self.trainer_cache[user_id].name,
                                                 quantity,
                                                 pkmn.title()))
                    await self._display_total_pokemon_caught()
        except Exception as e:
            error_msg = 'Failed to release pokemon: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def display_pinventory(self, ctx, page_number):
        """
        Displays pokemon inventory
        """
        try:
            trainer_id = ctx.message.author.id
            if ctx.message.author.id not in self.trainer_data:
                await self.bot.say("Trainer has nothing to display.")
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
                    for legend in self.legendary_pkmn:
                        if legend in pkmn[0]:
                            pkmn_result = "**{}** x{}\n".format(pkmn[0].title(),
                                                                pkmn[1])
                    if pkmn[0] in self.ultra_pkmn:
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
                await self.bot.say("Page number is invalid.")
                return
            msg = ("__**{}** Pokémon total. "
                   "(Page **{} of {}**)__\n"
                   "".format(pinventory_count, page_number, max_pages)
                   + msg)
            em = discord.Embed(title="{}'s Inventory".format(user),
                               description=msg,
                               colour=0xff0000)
            try:
                await self.bot.say(embed=em)
            except:
                pass
        except Exception as e:
            print("An error has occured in displaying inventory. "
                  "See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def display_gif(self, pkmn_name, shiny):
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
            await self.bot.say(embed=em)
        except Exception as e:
            print("An error has occured in displaying a gif. "
                  "See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def display_trainer_profile(self, trainer):
        """
        Gets trainer profile of a trainer specified

        @param trainer - trainer to look up
        """
        try:
            if not self.trainer_cache:
                await self.bot.say("Trainer data is still loading. "
                                   "Please wait and try again later.")
                return
            trainer_id = re.search(r'\d+', trainer)
            trainer_id = trainer_id.group(0)
            if trainer_id not in self.trainer_cache:
                await self.bot.say("Failed to find the trainer profile for "
                                   "the trainer specified.")
                return
            else:
                user_obj = self.trainer_cache[trainer_id]
            legendary_pkmn_count = 0
            ultra_pkmn_count = 0
            shiny_pkmn_count = 0
            total_pkmn_count = 0
            if trainer_id in self.trainer_data:
                pinventory = self.trainer_data[trainer_id]["pinventory"]
                for pkmn in pinventory:
                    for legend in self.legendary_pkmn:
                        if legend in pkmn:
                            legendary_pkmn_count += pinventory[pkmn]
                    if pkmn in self.ultra_pkmn:
                        ultra_pkmn_count += pinventory[pkmn]
                    if "Shiny" in pkmn:
                        shiny_pkmn_count += pinventory[pkmn]
                    total_pkmn_count += pinventory[pkmn]
            else:
                await self.bot.say("Trainer hasn't set off on his journey to "
                                   "catch 'em all yet.")
                return
            em = discord.Embed()
            em.set_author(name=user_obj)
            em.set_thumbnail(url=user_obj.avatar_url)
            em.add_field(name="Legendary Pokémon caught",
                         value=legendary_pkmn_count)
            em.add_field(name="Ultra Pokémon caught",
                         value=ultra_pkmn_count)
            em.add_field(name="Shiny Pokémon caught︀",
                         value=shiny_pkmn_count)
            em.add_field(name="Total Pokémon caught",
                         value=total_pkmn_count)
            await self.bot.say(embed=em)
        except Exception as e:
            print("An error has occured in displaying trainer profile. "
                  "See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def _check_cooldown(self, ctx, current_time):
        """
        Checks if cooldown has passed
        True if cooldown is still active
        False if cooldown is not active
        """
        user_id = ctx.message.author.id
        timer = float(self.trainer_data[user_id]["timer"])
        happy_hour_event = self.event.event_data["happy_hour_event"]
        cooldown_limit = datetime.timedelta(seconds=self.cooldown_seconds)
        time_passed = datetime.timedelta(seconds=time.time()-timer)
        current_cooldown = cooldown_limit.total_seconds() - time_passed.total_seconds()
        converted_cooldown = datetime.timedelta(seconds=current_cooldown)
        if self.event.happy_hour:
            converted_cooldown_seconds = converted_cooldown.total_seconds()/happy_hour_event["cooldown_divider"]
            converted_cooldown = datetime.timedelta(seconds=converted_cooldown_seconds)
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
            await self.bot.say(msg)
            return True

    async def _post_pokemon_catch(self, ctx, random_pkmn, pkmn_img_path, random_pkmnball, is_shiny, hatched=False):
        """
        Posts the pokemon that was caught
        """
        try:
            EGG_MANAPHY = "egg-manaphy"
            ctx_channel = ctx.message.channel
            user = "**{}**".format(ctx.message.author.name)
            catch_condition = "caught" if not hatched else "hatched"
            msg = ("{} {} a {}**{}**!"
                   "".format(user,
                             catch_condition,
                             random_pkmnball,
                             random_pkmn.replace('_', ' ').title()))
            legendary = False
            special_channel = None
            for legend in self.legendary_pkmn:
                if random_pkmn is EGG_MANAPHY:
                    break
                if legend in random_pkmn:
                    legendary = True
            if legendary or random_pkmn in self.ultra_pkmn:
                for channel in ctx.message.server.channels:
                    if legendary:
                        if "legendary" == channel.name:
                            special_channel = self.bot.get_channel(channel.id)
                            break
                    else:
                        if "ultra" == channel.name:
                            special_channel = self.bot.get_channel(channel.id)
                            break
                if special_channel is not None:
                    em = discord.Embed(description=msg,
                                       colour=0xFFFFFF)
                    if is_shiny:
                        em.set_thumbnail(url="https://raw.githubusercontent.com/msikma/"
                                             "pokesprite/master/icons/pokemon/shiny/"
                                             "{}.png"
                                             "".format(random_pkmn.replace('_', '-')))
                        em.set_image(url="https://play.pokemonshowdown.com/sprites/"
                                         "xyani-shiny/{}.gif"
                                         "".format(random_pkmn.replace('_', '')))
                    else:
                        em.set_thumbnail(url="https://raw.githubusercontent.com/msikma/"
                                             "pokesprite/master/icons/pokemon/regular/"
                                             "{}.png"
                                             "".format(random_pkmn.replace('_', '-')))
                        em.set_image(url="https://play.pokemonshowdown.com/sprites/"
                                         "xyani/{}.gif"
                                         "".format(random_pkmn.replace('_', '')))
                    try:
                        await self.bot.send_message(special_channel,
                                                    embed=em)
                    except:
                        pass
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
                if shiny_channel is not None:
                    em = discord.Embed(description=msg,
                                       colour=0xFFFFFF)
                    em.set_thumbnail(url="https://raw.githubusercontent.com/msikma/"
                                         "pokesprite/master/icons/pokemon/shiny/"
                                         "{}.png"
                                         "".format(base_pkmn.replace('_', '-')))
                    em.set_image(url="https://play.pokemonshowdown.com/sprites/"
                                     "xyani-shiny/{}.gif"
                                     "".format(base_pkmn.replace('_', '')))
                    try:
                        await self.bot.send_message(shiny_channel,
                                                    embed=em)
                    except:
                        pass
            try:
                await self.bot.send_file(destination=ctx_channel,
                                         fp=pkmn_img_path,
                                         content=msg)
            except:
                pass
        except Exception as e:
            print("An error has occured in posting catch. See error.log.")
            logger.error("Exception: {}".format(str(e)))

    async def catch_pokemon(self, ctx):
        """
        Generates a random pokemon to be caught
        """
        try:
            current_time = time.time()
            user_id = ctx.message.author.id
            if user_id not in self.trainer_data:
                user_obj = await self.bot.get_user_info(user_id)
                self.trainer_data[user_id] = {}
                self.trainer_data[user_id]["pinventory"] = {}
                self.trainer_data[user_id]["timer"] = False
                self.trainer_cache[user_id] = user_obj
            if not await self._check_cooldown(ctx, current_time):
                shiny_rng = random.uniform(0, 1)
                if shiny_rng < self.shiny_rate:
                    random_pkmn = random.choice(list(self.shiny_pokemon.keys()))
                    pkmn_img_path = self.shiny_pokemon[random_pkmn][0]
                    is_shiny = True
                else:
                    random_pkmn = random.choice(list(self.nrml_pokemon.keys()))
                    pkmn_img_path = self.nrml_pokemon[random_pkmn][0]
                    is_shiny = False
                random_pkmnball = random.choice(list(self.pokeball))
                trainer_profile = self.trainer_data[user_id]
                trainer_profile["timer"] = current_time
                if random_pkmn not in trainer_profile["pinventory"]:
                    if is_shiny:
                        trainer_profile["pinventory"][random_pkmn+"(Shiny)"] = 1
                    else:
                        trainer_profile["pinventory"][random_pkmn] = 1
                else:
                    if is_shiny:
                        pokemon_count = int(trainer_profile["pinventory"][random_pkmn+"(Shiny)"])
                        trainer_profile["pinventory"][random_pkmn+"(Shiny)"] = pokemon_count+1
                    else:
                        pokemon_count = int(trainer_profile["pinventory"][random_pkmn])
                        trainer_profile["pinventory"][random_pkmn] = pokemon_count+1
                self._save_trainer_file(self.trainer_data)
                await self._display_total_pokemon_caught()
                await self._post_pokemon_catch(ctx,
                                               random_pkmn,
                                               pkmn_img_path,
                                               random_pkmnball,
                                               is_shiny)
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
        for legend in self.legendary_pkmn:
            if legend in pkmn:
                return False
        if pkmn in self.ultra_pkmn:
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
            user_id = ctx.message.author.id
            if user_id in self.trainer_data:
                pinventory = self.trainer_data[user_id]["pinventory"]
                if egg in pinventory:
                    shiny_rng = random.uniform(0, 1)
                    if shiny_rng < self.shiny_rate*self.shiny_hatch_multiplier:
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
                    if shiny_rng < self.shiny_rate*self.shiny_hatch_multiplier:
                        pkmn_img_path = self.shiny_pokemon[random_pkmn][0]
                        is_shiny = True
                    else:
                        pkmn_img_path = self.nrml_pokemon[random_pkmn][0]
                        is_shiny = False
                    pinventory[egg_manaphy] -= 1
                    if pinventory[egg_manaphy] < 1:
                        pinventory.pop(egg_manaphy)
                else:
                    await self.bot.say("There are no eggs in the trainer's "
                                       "inventory.")
                    return
                random_pkmnball = random.choice(list(self.pokeball))
                self._save_trainer_file(self.trainer_data)
                await self._post_pokemon_catch(ctx,
                                               random_pkmn,
                                               pkmn_img_path,
                                               random_pkmnball,
                                               is_shiny,
                                               hatched=True)
            else:
                await self.bot.say("Trainer hasn't set off on his journey to "
                                   "catch 'em all yet.")
        except Exception as e:
            print("An error has occured in hatching egg. See error.log.")
            logger.error("Exception: {}".format(str(e)))
