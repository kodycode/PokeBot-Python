from classes import PokeBotModule, Pokemon
from math import ceil
from modules.legendary_pokemon_service import LegendaryPokemonService
from modules.pokebot_assets import PokeBotAssets
from modules.pokebot_exceptions import (
    CatchCooldownIncompleteException,
    HigherPageSpecifiedException,
    HigherReleaseQuantitySpecifiedException,
    InventoryLogicException,
    UnregisteredTrainerException
)
from modules.pokebot_rates import PokeBotRates
from modules.trainer_service import TrainerService
from modules.ultra_beasts_service import UltraBeastsService
from utils import format_pokemon_name, get_ctx_user_id, get_specific_text_channel
import discord
import random
import time


class InventoryLogic(PokeBotModule):
    """Handles the basic logic of features for PokeBot"""

    SHINY_ICON_URL = "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/shiny/"
    SHINY_GIF_URL = "https://play.pokemonshowdown.com/sprites/xyani-shiny/"
    NRML_ICON_URL = "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/"
    NRML_GIF_URL = "https://play.pokemonshowdown.com/sprites/xyani/"
    PKMN_PER_PAGE = 20

    def __init__(self, bot):
        self.assets = PokeBotAssets()
        self.bot = bot
        self.legendary_service = LegendaryPokemonService()
        self.pokebot_rates = PokeBotRates(bot)
        self.trainer_service = TrainerService(bot, self.pokebot_rates)
        self.total_pokemon_caught = self.trainer_service.get_total_pokemon_caught()
        self.ultra_beasts = UltraBeastsService()

    async def catch_pokemon(self, ctx: discord.ext.commands.Context) -> None:
        """
        Generates a random pokemon to be caught
        """
        try:
            catch_condition = "caught"
            current_time = time.time()
            user_id = get_ctx_user_id(ctx)
            seconds_left_to_catch = \
                self.trainer_service.get_time_left_to_catch(user_id)
            if seconds_left_to_catch <= 0:
                random_pkmn = self._generate_random_pokemon()
                self.trainer_service.give_pokemon_to_trainer(
                    user_id,
                    random_pkmn,
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
            else:
                raise CatchCooldownIncompleteException(seconds_left_to_catch)
        except CatchCooldownIncompleteException:
            raise
        except Exception as e:
            msg = "Error has occurred in catching pokemon."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

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
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

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
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

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
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

    async def _display_total_pokemon_caught(self) -> None:
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
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

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
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

    async def _post_pokemon_catch(
        self,
        ctx: discord.ext.commands.Context,
        pkmn: Pokemon,
        catch_condition: str,
        lootbox: str
    ) -> None:
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
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

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
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

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
            if pkmn.is_legendary or pkmn.is_ultra_beast:
                await self._post_catch_to_special_channel(ctx, "special", pkmn, msg)
            if pkmn.is_shiny:
                await self._post_catch_to_special_channel(ctx, "shiny", pkmn, msg)
            await channel.send(file=discord.File(pkmn.img_path), content=msg)
        except Exception as e:
            msg = "Error has occurred in posting catch to channels."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

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
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)

    async def display_pinventory(
        self,
        ctx: discord.ext.commands.Context,
        page: int
    ):
        """
        Creates and displays the trainer's pokemon inventory
        """
        try:
            user_id = get_ctx_user_id(ctx)
            valid_user = self.trainer_service.check_existing_trainer(user_id)
            if not valid_user:
                raise UnregisteredTrainerException()
            username = ctx.message.author.name
            pinventory = \
                await self.trainer_service.get_trainer_inventory(user_id)
            pinventory_key_count = len(pinventory)
            max_page = \
                ceil(pinventory_key_count/20) if pinventory_key_count != 0 else 1
            if page > max_page:
                raise HigherPageSpecifiedException(max_page)
            current_list_of_pkmn_to_display = \
                await self._slice_pinventory_to_display(pinventory, page, max_page)
            pinventory_msg = await self._build_pinventory_msg_(
                current_list_of_pkmn_to_display,
                pinventory_key_count,
                page,
                max_page
            )
            em = discord.Embed(title="{}'s Inventory".format(username),
                               description=pinventory_msg,
                               colour=0xff0000)
            await ctx.send(embed=em)
        except HigherPageSpecifiedException as e:
            raise
        except Exception as e:
            msg = "Error has occurred in displaying inventory."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)          

    async def _slice_pinventory_to_display(
        self,
        pinventory: dict,
        page: int,
        max_page: int
    ) -> list:
        """
        Slices the pokemon inventory to display the number of pokemon to
        show from the trainer's inventory
        """
        try:
            lowest_pkmn_index = (page-1) * self.PKMN_PER_PAGE
            highest_pkmn_index = min(max_page*20, max(lowest_pkmn_index,1)*20)
            sorted_pokemon_inventory = sorted(pinventory.items())
            return sorted_pokemon_inventory[lowest_pkmn_index:highest_pkmn_index]
        except Exception as e:
            msg = "Error has occurred in slicing pinventory."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)  

    async def _build_pinventory_msg_(
        self,
        current_list_of_pkmn_to_display: list,
        pinventory_key_count: int,
        page: int,
        max_page: int
    ) -> str:
        """
        Builds the bot message for the trainer's pokemon inventory display
        """
        try:
            list_of_pkmn_msg = ""
            for pkmn in current_list_of_pkmn_to_display:
                pkmn_result = ''
                is_legendary = \
                    self.legendary_service.is_pokemon_legendary(pkmn[0])
                is_ultra_beast = \
                    self.ultra_beasts.is_pokemon_ultra_beast(pkmn[0])
                if is_legendary or is_ultra_beast:
                    pkmn_result = f"**{pkmn[0].title()}** x{pkmn[1]}\n"
                    list_of_pkmn_msg += pkmn_result
                else:
                    list_of_pkmn_msg += f"{pkmn[0].title()} x{pkmn[1]}\n"
            display_total_hdr = (f"__**{pinventory_key_count}** Pokémon total."
                                 f" (Page **{page} of {max_page}**)__\n")
            return display_total_hdr + list_of_pkmn_msg
        except Exception as e:
            msg = "Error has occurred in building pinventory message."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e)  

    async def release_pokemon(
        self,
        ctx: discord.ext.commands.Context,
        pkmn_name: str,
        quantity: int
    ) -> None:
        """
        Deletes a pokemon from the trainer's inventory
        """
        try:
            user_id = get_ctx_user_id(ctx)
            pkmn_lowercase = pkmn_name.lower()
            await self.trainer_service.decrease_pokemon_quantity(
                user_id,
                pkmn_lowercase,
                quantity
            )
        except HigherReleaseQuantitySpecifiedException:
            raise
        except Exception as e:
            msg = "Error has occurred in releasing pokemon."
            self.post_error_log_msg(InventoryLogicException.__name__, msg, e) 
