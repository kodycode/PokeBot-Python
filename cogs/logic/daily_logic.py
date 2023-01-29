from classes import PokeBotModule
from modules.pokebot_exceptions import (
    DailyLogicException,
    DailyCooldownIncompleteException
)
from modules.pokebot_rates import PokeBotRates
from modules.pokebot_lootbox import PokeBotLootbox
from modules.services.trainer_service import TrainerService
from utils import get_ctx_user_id
import datetime
import discord
import time


class DailyLogic(PokeBotModule):
    """
    Handles logic for daily commands
    """

    def __init__(self, bot):
        self.rates = PokeBotRates(bot)
        self.lootbox = PokeBotLootbox(self.rates)
        self.trainer_service = TrainerService(self.rates)
    
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
            daily_lootbox = self.lootbox.generate_lootbox(daily=True)
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
                self.trainer_service.get_trainer_last_daily_redeemed_time(user_id)
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
            msg = (f"Error has occurred in checking user daily "
                   "claim ({user_id}).")
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
            em = discord.Embed()
            msg = (f"{ctx.message.author.mention}, you have **{daily_tokens}**"
                   " daily tokens")
            return msg
        except Exception as e:
            msg = ("Error has occurred in building message for displaying"
                   f" the users daily tokens ({user_id}).")
            self.post_error_log_msg(DailyLogicException.__name__, msg, e)
            raise
