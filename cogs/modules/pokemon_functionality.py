from bot_logger import logger
from collections import defaultdict
from math import ceil
from pokeball import POKEBALL_LIST
from legendary import LEGENDARY_PKMN, ULTRA_PKMN
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
        self.nrml_pokemon = self._load_pokemon_imgs()
        self.shiny_pokemon = self._load_pokemon_imgs(shiny=True)
        self.trainer_data = self._check_trainer_file()
        self._save_trainer_file(self.trainer_data, backup=True)

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
            await self.bot.say("Reload complete.")
        except Exception as e:
            error_msg = 'Failed to reload: {}'.format(str(e))
            print(error_msg)
            logger.error(error_msg)

    async def display_pinventory(self, ctx, page_number):
        """
        Displays pokemon inventory
        """
        try:
            if ctx.message.author.id not in self.trainer_data:
                await self.bot.say("Trainer has nothing to display.")
                return
            if page_number <= 1:
                page_number = 1
            user = ctx.message.author.name
            user_id = ctx.message.author.id
            pinventory = self.trainer_data[user_id]["pinventory"]
            pinventory_count = 0
            msg = ''
            i = (page_number-1)*20
            count = 0
            for pkmn in sorted(pinventory.items()):
                if i <= count and i < 20*page_number:
                    msg += "{} x{}\n".format(pkmn[0].title(), pkmn[1])
                    i += 1
                pinventory_count += int(pkmn[1])
                count += 1
            max_pages = ceil(pinventory_count/20)
            if max_pages == 0:
                max_pages = 1
            if page_number > max_pages:
                await self.bot.say("Page number is invalid.")
                return
            msg = ("__**{}'s Pokemon**__: Includes **{}** Pokemon. "
                   "[Page **{}/{}**]\n"
                   "".format(user, pinventory_count, page_number, max_pages)
                   + msg)
            try:
                await self.bot.say(msg)
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

    async def _check_cooldown(self, ctx, current_time):
        """
        Checks if cooldown has passed
        True if cooldown is still active
        False if cooldown is not active
        """
        user = ctx.message.author.name
        user_id = ctx.message.author.id
        timer = float(self.trainer_data[user_id]["timer"])
        cooldown_time = time.time() - timer
        hours = int(cooldown_time // 3600)
        minutes = int((cooldown_time % 3600) // 60)
        seconds = int(cooldown_time % 60)
        if minutes >= 10 or hours >= 1:
            return False
        else:
            msg = ":no_entry_sign:**{}**, you need to wait another ".format(user)
            msg += "**{} minutes &** ".format(str(9-minutes))
            msg += "**{} seconds** ".format(str(60-seconds))
            msg += "before catching another pokemon."
            await self.bot.say(msg)
            return True

    async def _post_pokemon_catch(self, ctx, user, random_pkmn, pkmn_img_path, random_pkmnball, is_shiny):
        """
        Posts the pokemon that was caught
        """
        try:
            ctx_channel = ctx.message.channel
            msg = ("{}, {} you've caught a "
                   "**{}**!".format(user,
                                    random_pkmnball,
                                    random_pkmn.replace('_', ' ').title()))
            legendary = False
            legendary_channel = None
            for legend in LEGENDARY_PKMN:
                if legend in random_pkmn:
                    legendary = True
            if legendary or random_pkmn in ULTRA_PKMN:
                for channel in ctx.message.server.channels:
                    if "legendary" == channel.name:
                        legendary_channel = self.bot.get_channel(channel.id)
                        break
                if legendary_channel is not None:
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
                        await self.bot.send_message(legendary_channel,
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
                self.trainer_data[user_id] = {}
                self.trainer_data[user_id]["pinventory"] = {}
                self.trainer_data[user_id]["timer"] = False
            if not await self._check_cooldown(ctx, current_time):
                shiny_rng = random.uniform(0, 1)
                if shiny_rng < 0.02:
                    random_pkmn = random.choice(list(self.shiny_pokemon.keys()))
                    pkmn_img_path = self.shiny_pokemon[random_pkmn][0]
                    is_shiny = True
                else:
                    random_pkmn = random.choice(list(self.nrml_pokemon.keys()))
                    pkmn_img_path = self.nrml_pokemon[random_pkmn][0]
                    is_shiny = False
                random_pkmnball = random.choice(list(POKEBALL_LIST))
                user = "**{}**".format(ctx.message.author.name)
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
                await self._post_pokemon_catch(ctx,
                                               user,
                                               random_pkmn,
                                               pkmn_img_path,
                                               random_pkmnball,
                                               is_shiny)
        except Exception as e:
            print("An error has occured in catching pokemon. See error.log.")
            logger.error("Exception: {}".format(str(e)))
