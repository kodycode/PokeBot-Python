from classes import PokeBotModule
from modules.pokebot_exceptions import (
    DailyLogicException,
    DailyCooldownIncompleteException,
    ImproperDailyShopItemNumberException,
    NotEnoughDailyShopTokensException
)
from modules.pokebot_assets import PokeBotAssets
from modules.pokebot_rates import PokeBotRates
from modules.pokebot_status import PokeBotStatus
from modules.pokebot_generator import PokeBotGenerator
from modules.services.trainer_service import TrainerService
from utils import get_ctx_user_id
import datetime
import discord
import time


class DailyLogic(PokeBotModule):
    """
    Handles logic for daily commands
    """

    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    SHINY = "shiny"

    ITEM_DESCRIPTION = "description"
    ITEM_PRICE = "price"

    def __init__(self, bot):
        self.assets = PokeBotAssets()
        self.rates = PokeBotRates(bot)
        self.status = PokeBotStatus(bot)
        self.generator = PokeBotGenerator(self.assets, self.rates)
        self.trainer_service = TrainerService(self.rates)
        self.daily_shop_menu = self.rates.get_daily_shop_menu()

    def claim_daily(
        self,
        ctx: discord.ext.commands.Context
    ) -> str:
        """
        Claims the daily lootbox for the trainer
        """
        try:
            current_time = time.time()
            user_id = get_ctx_user_id(ctx)
            if not self._check_user_daily_redemption(user_id):
                raise DailyCooldownIncompleteException()
            daily_lootbox = self.generator.generate_lootbox(daily=True)
            self.trainer_service.give_lootbox_to_trainer(
                user_id,
                daily_lootbox,
            )
            self.trainer_service.set_trainer_last_daily_redeemed_time(
                user_id,
                current_time
            )
            self.trainer_service.increment_trainer_daily_token_count(user_id)
            self.trainer_service.save_all_trainer_data()
            return daily_lootbox.title()
        except DailyCooldownIncompleteException:
            raise
        except Exception as e:
            msg = ("Error has occurred in claiming daily from "
                   f"trainer ({user_id}).")
            self.post_error_log_msg(DailyLogicException.__name__, msg, e)
            raise

    def _check_user_daily_redemption(
        self,
        user_id: str
    ) -> bool:
        """
        Checks if the user can use the daily command
        """
        try:
            # get user daily time
            trainer_last_daily_redeemed_time = \
                self.trainer_service.get_trainer_last_daily_redeemed_time(
                    user_id
                )
            datetime_last_daily_redeemed_time = datetime.datetime.fromtimestamp(
                trainer_last_daily_redeemed_time
            )
            # get daily claim reset time
            reset_hour = self.rates.get_daily_redemption_reset_hour()
            datetime_reset_hour = datetime.time(reset_hour, 0, 0)
            reset_time = datetime.datetime.combine(
                datetime.date.today(),
                datetime_reset_hour
            )
            if datetime_last_daily_redeemed_time < reset_time:
                return True
            return False
        except Exception as e:
            msg = ("Error has occurred in checking user daily "
                   f"claim ({user_id}).")
            self.post_error_log_msg(DailyLogicException.__name__, msg, e)
            raise

    def build_daily_tokens_msg(
        self,
        ctx: discord.ext.commands.Context
    ) -> str:
        """
        Builds the message to tell the user how many daily tokens they have
        """
        try:
            user_id = get_ctx_user_id(ctx)
            daily_tokens = self.trainer_service.get_daily_tokens(user_id)
            msg = (f"{ctx.message.author.mention}, you have **{daily_tokens}**"
                   " daily tokens")
            return msg
        except Exception as e:
            msg = ("Error has occurred in building message for displaying"
                   f" the users daily tokens ({user_id}).")
            self.post_error_log_msg(DailyLogicException.__name__, msg, e)
            raise

    def get_daily_shop_info(
        self
    ) -> discord.Embed:
        """
        Gets the info on what's available in the daily shop
        """
        try:
            menu_items = ""
            item_count = 1
            for item in self.daily_shop_menu:
                item_price = self.daily_shop_menu[item][self.ITEM_PRICE]
                item_description = self.daily_shop_menu[item][self.ITEM_DESCRIPTION]
                menu_items += (f"[{item_count}] - **{item_description}**"
                               f" - **{item_price}** tokens\n")
                item_count += 1
            em = discord.Embed(title="Daily Token Shop",
                               description=menu_items,
                               colour=0xFFFF00)
            return em
        except Exception as e:
            msg = "Error has occurred in getting daily shop info"
            self.post_error_log_msg(DailyLogicException.__name__, msg, e)
            raise

    async def buy_daily_shop_item(
        self,
        ctx: discord.ext.commands.Context,
        item_num: int
    ) -> str:
        """
        Buys the item listed in the daily shop
        """
        try:
            user_id = get_ctx_user_id(ctx)
            item_index = item_num - 1
            num_daily_shop_items = len(self.daily_shop_menu)
            if item_index < 0 or item_index > num_daily_shop_items:
                raise ImproperDailyShopItemNumberException(
                    num_daily_shop_items
                )
            daily_shop_items_keys = list(self.daily_shop_menu.keys())
            daily_shop_item_key = daily_shop_items_keys[item_index]
            item_price = \
                self.daily_shop_menu[daily_shop_item_key][self.ITEM_PRICE]
            daily_tokens = self.trainer_service.get_daily_tokens(user_id)
            if daily_tokens < item_price:
                raise NotEnoughDailyShopTokensException(item_price)
            daily_tokens_left = daily_tokens - item_price
            self.trainer_service.set_daily_tokens_amount(
                user_id,
                daily_tokens_left
            )
            item_description = \
                await self._give_daily_shop_item_to_trainer(
                    user_id,
                    daily_shop_item_key
                )
            self.trainer_service.save_all_trainer_data()
            msg = (f"{ctx.message.author.mention} purchased a"
                   f" **{item_description.title()}** from"
                   " the daily shop.")
            return msg
        except ImproperDailyShopItemNumberException:
            raise
        except NotEnoughDailyShopTokensException:
            raise
        except Exception as e:
            msg = "Error has occurred in buying daily shop item"
            self.post_error_log_msg(DailyLogicException.__name__, msg, e)
            raise

    async def _give_daily_shop_item_to_trainer(
        self,
        user_id: str,
        item_key: str
    ) -> str:
        """
        Gives the daily shop item to the trainer
        """
        try:
            if item_key == "bronze" or \
               item_key == "silver" or \
               item_key == "gold":
                self.trainer_service.give_lootbox_to_trainer(user_id, item_key)
            elif item_key == "shiny":
                random_pkmn = self.generator.generate_random_pokemon(
                    is_shiny=True
                )
                self.trainer_service.give_pokemon_to_trainer(
                    user_id,
                    random_pkmn
                )
                self.status.increase_total_pkmn_count(1)
                await self.status.display_total_pokemon_caught()
                return f"(Shiny) {random_pkmn.name}"
            return self.daily_shop_menu[item_key][self.ITEM_DESCRIPTION]
        except Exception as e:
            msg = ("Failed to give the daily shop item to a"
                   f" trainer {user_id}")
            self.post_error_log_msg(DailyLogicException.__name__, msg, e)
            raise
