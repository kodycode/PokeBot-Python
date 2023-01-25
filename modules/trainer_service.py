from database import TrainerDAO
from discord.ext import commands
from modules.pokebot_rates import PokeBotRates
import time


class TrainerService:
    def __init__(self, bot: commands.Bot, rates: PokeBotRates) -> None:
        self.trainer_dao = TrainerDAO()
        self.rates = rates

    def give_pokemon_to_trainer(self, user_id: str, pkmn_name: str, ):
        """
        Gives the pokemon to the trainer in their inventory
        """
        self._check_and_create_new_trainer(user_id)
        self.trainer_dao.increment_pokemon_quantity(user_id, pkmn_name)

    def _check_and_create_new_trainer(self, user_id: str):
        """
        Checks to see if the User ID is a new to the list
        of trainers and generates a new trainer object within
        the list for the user
        """
        if not self.trainer_dao.is_existing_trainer(user_id):
            self.trainer_dao.generate_new_trainer(user_id)

    def validate_trainer_catch(self, user_id: str):
        """
        Validates whether the trainer is able to catch a
        pokemon or not
        """
        current_time = time.time()
        trainer_last_catch_time = \
            self.trainer_dao.get_last_catch_time(user_id)

        # If time has passed beyond the amount of seconds to wait,
        # return True
        time_since_last_catch = current_time - trainer_last_catch_time
        if time_since_last_catch > self.rates.get_catch_cooldown_seconds():
            return True
        return False

    def save_all_trainer_data(self):
        """
        Saves all trainer data
        """
        self.trainer_dao.save()
        
    def set_trainer_last_catch_time(self, user_id: str, time: float) -> None:
        """
        Sets the last catch time of the trainer
        """
        self.trainer_dao.set_last_catch_time(user_id, time)

    def give_lootbox_to_trainer(self, user_id: str, lootbox: str):
        """
        Gives a lootbox to the trainer in their inventory
        """
        self._check_and_create_new_trainer(user_id)
        self.trainer_dao.increment_lootbox_quantity(user_id, lootbox)

    def get_total_pokemon_caught(self) -> int:
        """
        Gets the total of all pokemon caught
        """
        return self.trainer_dao.get_total_pokemon_caught()
