from database import TrainerDAO
from modules import PokeBotRates
import time


class PokeBotTrainerService:
    def __init__(self) -> None:
        self.trainer_dao = TrainerDAO()
        self.rates = PokeBotRates()

    def give_pokemon_to_trainer(self, pkmn_name: str, user_id: str):
        """
        Gives the pokemon to the trainer in their inventory
        """
        self._check_and_create_new_trainer(user_id)

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
        
    def set_trainer_last_catch_time(self, user_id: str, time: float) -> None:
        """
        Sets the last catch time of the trainer
        """
        self.trainer_dao.set_last_catch_time(user_id, time)
