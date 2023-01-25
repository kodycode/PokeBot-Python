from bot_logger import logger
from classes import PokeBotModule
from database import TrainerDAO
from discord.ext import commands
from modules.pokebot_rates import PokeBotRates
import discord
import time


class TrainerServiceException(Exception):
    pass


class TrainerService(PokeBotModule):
    def __init__(self, bot: commands.Bot, rates: PokeBotRates) -> None:
        self.trainer_dao = TrainerDAO()
        self.rates = rates

    def give_pokemon_to_trainer(self, user_id: str, pkmn_name: str):
        """
        Gives the pokemon to the trainer in their inventory
        """
        try:
            self._check_and_create_new_trainer(user_id)
            self.trainer_dao.increment_pokemon_quantity(user_id, pkmn_name)
        except Exception as e:
            msg = "Error has occurred in creating catch msg."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)

    def _check_and_create_new_trainer(self, user_id: str):
        """
        Checks to see if the User ID is a new to the list
        of trainers and generates a new trainer object within
        the list for the user
        """
        try:
            if not self.trainer_dao.is_existing_trainer(user_id):
                self.trainer_dao.generate_new_trainer(user_id)
        except Exception as e:
            msg = "Error has occurred in checking and creating new trainer."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)

    def validate_trainer_catch(self, user_id: str):
        """
        Validates whether the trainer is able to catch a
        pokemon or not
        """
        try:
            current_time = time.time()
            trainer_last_catch_time = \
                self.trainer_dao.get_last_catch_time(user_id)

            # If time has passed beyond the amount of seconds to wait,
            # return True
            time_since_last_catch = current_time - trainer_last_catch_time
            if time_since_last_catch > self.rates.get_catch_cooldown_seconds():
                return True
            return False
        except Exception as e:
            msg = "Error has occurred in validating trainer catch."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)

    def save_all_trainer_data(self):
        """
        Saves all trainer data
        """
        try:
            self.trainer_dao.save()
        except Exception as e:
            msg = "Error has occurred in saving all trainer data."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
        
    def set_trainer_last_catch_time(self, user_id: str, time: float) -> None:
        """
        Sets the last catch time of the trainer
        """
        try:
            self.trainer_dao.set_last_catch_time(user_id, time)
        except Exception as e:
            msg = "Error has occurred in setting last_catch_time."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)

    def give_lootbox_to_trainer(self, user_id: str, lootbox: str):
        """
        Gives a lootbox to the trainer in their inventory
        """
        try:
            self._check_and_create_new_trainer(user_id)
            self.trainer_dao.increment_lootbox_quantity(user_id, lootbox)
        except Exception as e:
            msg = "Error has occurred in giving lootbox to trainer."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)

    def get_total_pokemon_caught(self) -> int:
        """
        Gets the total of all pokemon caught
        """
        try:
            return self.trainer_dao.get_total_pokemon_caught()
        except Exception as e:
            msg = "Error has occurred in getting total pokemon caught."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
