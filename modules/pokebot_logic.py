from bot_logger import logger
from classes import PokeBotModule, Pokemon
from modules.legendary_pokemon_service import LegendaryPokemonService
from modules.pokebot_assets import PokeBotAssets
from modules.pokebot_rates import PokeBotRates
from modules.trainer_service import TrainerService
from modules.ultra_beasts_service import UltraBeastsService
from utils import format_pokemon_name, get_ctx_user_id, get_specific_text_channel
import discord
import random
import time


class PokeBotLogicException(Exception):
    pass


class PokeBotLogic(PokeBotModule):
    """Handles the basic logic of features for PokeBot"""

    SHINY_ICON_URL = "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/shiny/"
    SHINY_GIF_URL = "https://play.pokemonshowdown.com/sprites/xyani-shiny/"
    NRML_ICON_URL = "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/"
    NRML_GIF_URL = "https://play.pokemonshowdown.com/sprites/xyani/"

    def __init__(self, bot):
        self.assets = PokeBotAssets()
        self.bot = bot
        self.legendary_service = LegendaryPokemonService()
        self.pokebot_rates = PokeBotRates(bot)
        self.trainer_service = TrainerService(bot, self.pokebot_rates)
        self.total_pokemon_caught = self.trainer_service.get_total_pokemon_caught()
        self.ultra_beasts_service = UltraBeastsService()

    async def catch_pokemon(self, ctx: discord.ext.commands.Context):
        """
        Generates a random pokemon to be caught
        """
        try:
            catch_condition = "caught"
            current_time = time.time()
            user_id = get_ctx_user_id(ctx)
            is_trainer_catching = \
                self.trainer_service.validate_trainer_catch(user_id)
            if is_trainer_catching:
                random_pkmn = self._generate_random_pokemon()
                self.trainer_service.give_pokemon_to_trainer(
                    user_id,
                    random_pkmn.name,
                )
                self.trainer_service.set_trainer_last_catch_time(
                    user_id,
                    current_time
                )
                lootbox = self._generate_lootbox()
                if lootbox:
                    self.trainer_service.give_lootbox_to_trainer(
                        user_id,
                        lootbox,
                    )
                await self._display_total_pokemon_caught()
                await self._post_pokemon_catch(ctx,
                                               random_pkmn,
                                               catch_condition,
                                               lootbox)
                self.trainer_service.save_all_trainer_data()
        except Exception as e:
            msg = "Error has occurred in catching pokemon."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)

    def _generate_random_pokemon(self) -> Pokemon:
        """
        Generates a random pokemon and returns a tuple of the
        pokemon name, image path, and whether the pokemon is shiny
        or not
        """
        try:
            self.total_pokemon_caught += 1
            is_shiny_pokemon = self._determine_shiny_pokemon()
            if is_shiny_pokemon:
                pkmn = self.assets.get_random_pokemon_asset(True)
            else:
                pkmn = self.assets.get_random_pokemon_asset()
            return pkmn
        except Exception as e:
            msg = "Error has occurred in generating pokemon."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)

    def _determine_shiny_pokemon(self) -> bool:
        """
        Determines the odds of a shiny pokemon 
        """
        try:
            shiny_rng_chance = random.uniform(0, 1)
            if shiny_rng_chance < self.pokebot_rates.get_shiny_pkmn_catch_rate():
                return True
            return False
        except Exception as e:
            msg = "Error has occurred in determining shiny pokemon."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)

    def _generate_lootbox(self, daily=False) -> str:
        """
        Generates a lootbox with consideration into daily or catch rates
        """
        try:
            lootbox_rng = random.uniform(0, 1)
            if daily:
                lootbox_bronze_rate = \
                    self.pokebot_rates.get_daily_lootbox_bronze_rate()
                lootbox_silver_rate = \
                    self.pokebot_rates.get_daily_lootbox_silver_rate()
                lootbox_gold_rate = \
                    self.pokebot_rates.get_daily_lootbox_gold_rate()
                lootbox_legendary_rate = \
                    self.pokebot_rates.get_daily_lootbox_legendary_rate()
            else:
                lootbox_bronze_rate = \
                    self.pokebot_rates.get_lootbox_bronze_rate()
                lootbox_silver_rate = \
                    self.pokebot_rates.get_lootbox_silver_rate()
                lootbox_gold_rate = self.pokebot_rates.get_lootbox_gold_rate()
                lootbox_legendary_rate = \
                    self.pokebot_rates.get_lootbox_legendary_rate()
            if lootbox_rng < lootbox_legendary_rate:
                return "legendary"
            elif lootbox_rng < lootbox_gold_rate:
                return "gold"
            elif lootbox_rng < lootbox_silver_rate:
                return "silver"
            elif lootbox_rng < lootbox_bronze_rate:
                return "bronze"
            return None
        except Exception as e:
            msg = "Error has occurred in generating lootbox."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)

    async def _display_total_pokemon_caught(self):
        """
        Iterates over trainer profiles and gets the total
        number of pokemon caught
        """
        try:
            total_pokemon_caught = \
                self.trainer_service.get_total_pokemon_caught()
            await self._update_game_status(total_pokemon_caught)
        except Exception as e:
            msg = "Failed to display total pokemon caught."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)

    async def _update_game_status(self, total_pkmn_count: int) -> None:
        """
        Updates the game status of the bot
        """
        try:
            game_status = discord.Game(name="{} Pokémon caught"
                                            "".format(total_pkmn_count))
            await self.bot.change_presence(activity=game_status)
        except Exception as e:
            msg = "Failed to update game status."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)

    async def _post_pokemon_catch(
        self,
        ctx: discord.ext.commands.Context,
        pkmn: Pokemon,
        catch_condition: str,
        lootbox: str
    ):
        """
        Posts the pokemon that was caught
        """
        try:
            random_pokeball = self.assets.get_random_pokeball_emoji()
            msg = await self._create_catch_message(
                ctx,
                pkmn,
                random_pokeball,
                catch_condition,
                lootbox
            )
            await self._post_catch_to_channels(ctx, pkmn, msg)
        except Exception as e:
            msg = "Error has occurred in posting catch."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)

    async def _create_catch_message(
        self,
        ctx: discord.ext.commands.Context, 
        pkmn: str, 
        random_pokeball: str, 
        catch_condition: str, 
        lootbox: str
    ):
        """
        Creates the catch message to display
        """
        try:
            formatted_pkmn_name = format_pokemon_name(pkmn.name)
            user = "**{}**".format(ctx.message.author.name)
            msg = f"{user} {catch_condition} a "\
                f"{random_pokeball}**{formatted_pkmn_name}**"
            msg += " and got a **{}** lootbox!".format(lootbox.title()) \
                if lootbox is not None else "!"
            return msg
        except Exception as e:
            msg = "Error has occurred in creating catch msg."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)

    async def _post_catch_to_channels(self,
        ctx: discord.ext.commands.Context,
        pkmn: Pokemon,
        msg: str
    ) -> None:
        """
        Posts to  bot channel about the pokemon catch and to the special
        and shiny channels if conditions are met about the random
        pokemon's status of being legendary, an ultra beast, or shiny
        """
        try:
            channel = ctx.message.channel
            is_legendary = \
                self.legendary_service.is_pokemon_legendary(pkmn.name)
            is_ultra_beast = \
                self.ultra_beasts_service.is_pokemon_ultra_beast(pkmn.name)
            if is_legendary or is_ultra_beast:
                await self._post_catch_to_special_channel(ctx, "special", pkmn, msg)
            if pkmn.is_shiny:
                await self._post_catch_to_special_channel(ctx, "shiny", pkmn, msg)
            await channel.send(file=discord.File(pkmn.img_path), content=msg)
        except Exception as e:
            msg = "Error has occurred in posting catch to channels."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)

    async def _post_catch_to_special_channel(
        self,
        ctx: discord.ext.commands.Command,
        channel_name: str,
        pkmn: Pokemon,
        msg: str):
        """
        Posts catch to special or certain channels (i.e. shiny, special)
        """
        try:
            formatted_pkmn_name = format_pokemon_name(pkmn.name).lower()
            channel = get_specific_text_channel(ctx, channel_name)
            if channel:
                em = discord.Embed(description=msg, colour=0xFFFFFF)
                if pkmn.is_shiny:
                    thumbnail = f"{self.SHINY_ICON_URL}{formatted_pkmn_name}.png"
                    image = f"{self.SHINY_GIF_URL}{formatted_pkmn_name}.gif"
                else:
                    thumbnail = f"{self.NRML_ICON_URL}{formatted_pkmn_name}.png"
                    image = f"{self.NRML_GIF_URL}{formatted_pkmn_name}.gif"
                em.set_thumbnail(url=thumbnail)
                em.set_image(url=image)
                await channel.send(embed=em)
        except Exception as e:
            msg = "Error has occurred in posting catch to all channels."
            self.post_error_log_msg(PokeBotLogicException.__name__, msg, e)
