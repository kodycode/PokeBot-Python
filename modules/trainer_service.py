from classes import PokeBotModule, Pokemon
from database import TrainerDAO
from discord.ext import commands
from modules.pokebot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    TrainerServiceException,
    UnregisteredTrainerException
)
from modules.pokebot_rates import PokeBotRates
import discord
import time


class TrainerService(PokeBotModule):

    # TODO: Put these lootbox names in a const file
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"

    def __init__(self, rates: PokeBotRates):
        self.trainer_dao = TrainerDAO()
        self.rates = rates

    def give_pokemon_to_trainer(self, user_id: str, pkmn: Pokemon) -> None:
        """
        Gives the pokemon to the trainer in their inventory
        """
        try:
            self._check_and_create_new_trainer(user_id)
            if pkmn.is_egg:
                if pkmn.name == "egg":
                    self.trainer_dao.increment_egg_count(user_id)
                elif pkmn.name == "egg-manaphy":
                    self.trainer_dao.increment_egg_manaphy_count(user_id)
            else:
                pkmn_name = pkmn.name
                if pkmn.is_shiny:
                    pkmn_name = "(shiny)" + pkmn_name
                self.trainer_dao.increment_pokemon_quantity(user_id, pkmn_name)
                if pkmn.is_legendary:
                    self.trainer_dao.increment_legendary_pkmn_count(user_id)
                elif pkmn.is_ultra_beast:
                    self.trainer_dao.increment_ultra_beasts_count(user_id)
                if pkmn.is_shiny:
                    self.trainer_dao.increment_shiny_pkmn_count(user_id)
                self.trainer_dao.increment_total_pkmn_count(user_id)
        except Exception as e:
            msg = "Error has occurred in creating catch msg."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def check_existing_trainer(self, user_id: str) -> bool:
        """
        Checks to see if the trainer profile exists or not
        """
        try:
            return self.trainer_dao.is_existing_trainer(user_id)
        except Exception as e:
            msg = "Error has occurred in checking and creating new trainer."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise


    def _check_and_create_new_trainer(self, user_id: str) -> None:
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
            raise

    def get_time_left_to_catch(self, user_id: str) -> int:
        """
        Validates whether the trainer is able to catch a
        pokemon or not
        """
        try:
            current_time = time.time()
            trainer_last_catch_time = \
                self.trainer_dao.get_last_catch_time(user_id)
            seconds_passed_since_last_catch = \
                current_time - trainer_last_catch_time
            catch_cooldown_seonds = self.rates.get_catch_cooldown_seconds()
            return int(catch_cooldown_seonds-seconds_passed_since_last_catch)
        except Exception as e:
            msg = ("Error has occurred in getting amount of seconds left to"
                  " catch")
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def save_all_trainer_data(self) -> None:
        """
        Saves all trainer data
        """
        try:
            self.trainer_dao.save()
        except Exception as e:
            msg = "Error has occurred in saving all trainer data."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise
        
    def set_trainer_last_catch_time(self, user_id: str, time: float) -> None:
        """
        Sets the last catch time of the trainer
        """
        try:
            self.trainer_dao.set_last_catch_time(user_id, time)
        except Exception as e:
            msg = "Error has occurred in setting last_catch_time."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def give_lootbox_to_trainer(self, user_id: str, lootbox: str) -> None:
        """
        Gives a lootbox to the trainer in their inventory
        """
        try:
            self._check_and_create_new_trainer(user_id)
            self.trainer_dao.increment_lootbox_quantity(user_id, lootbox)
        except Exception as e:
            msg = "Error has occurred in giving lootbox to trainer."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def get_total_pokemon_caught(self) -> int:
        """
        Gets the total of all pokemon caught
        """
        try:
            return self.trainer_dao.get_total_pokemon_caught()
        except Exception as e:
            msg = "Error has occurred in getting total pokemon caught."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def get_trainer_total_pokemon_caught(self, user_id: str) -> int:
        """
        Gets the trainer's total pokemon caught
        """
        try:
            return self.trainer_dao.get_total_pkmn_count(user_id)
        except Exception as e:
            msg = "Error has occurred in getting trainer total pokemon."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    async def display_trainer_profile(
        self,
        user_obj: discord.User
    ) -> discord.Embed:
        """
        Gets trainer profile of a trainer specified
        """
        try:
            user_id = str(user_obj.id)
            if not self.trainer_dao.is_existing_trainer(user_id):
                raise UnregisteredTrainerException()
            legendary_pkmn_count = self.trainer_dao.get_legendary_pkmn_count(user_id)
            ultra_beasts_count = self.trainer_dao.get_ultra_beasts_count(user_id)
            shiny_pkmn_count = self.trainer_dao.get_shiny_pkmn_count(user_id)
            total_pkmn_count = self.trainer_dao.get_total_pkmn_count(user_id)
            em = discord.Embed()
            em.set_author(name=user_obj)
            em.set_thumbnail(url=user_obj.avatar)
            em.add_field(name="Legendary Pokémon caught",
                        value=legendary_pkmn_count)
            em.add_field(name="Ultra Beasts caught",
                        value=ultra_beasts_count)
            em.add_field(name="Shiny Pokémon caught︀",
                        value=shiny_pkmn_count)
            em.add_field(name="Total Pokémon caught",
                        value=total_pkmn_count)
            return em
        except UnregisteredTrainerException:
            raise
        except Exception as e:
            msg = "Error has occurred in displaying trainer profile. "
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    async def get_trainer_inventory(self, user_id: str) -> dict:
        """
        Gets the trainer inventory given the user id
        """
        try:
            return self.trainer_dao.get_pokemon_inventory(user_id)
        except Exception as e:
            msg = "Error has occurred in getting trainer inventory."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    async def decrease_pokemon_quantity(
        self,
        user_id: str,
        pkmn: Pokemon,
        quantity: int
    ) -> None:
        """
        Deletes a pokemon from the trainer's inventory
        """
        try:
            pkmn_name = pkmn.name
            if pkmn.is_shiny:
                pkmn_name = "(shiny)" + pkmn_name
            pokemon_quantity = \
                self.trainer_dao.get_pokemon_quantity(user_id, pkmn_name)
            if quantity > pokemon_quantity:
                raise HigherReleaseQuantitySpecifiedException(pokemon_quantity)
            new_pokemon_quantity = pokemon_quantity - quantity
            self.trainer_dao.set_pokemon_quantity(
                user_id,
                pkmn_name,
                new_pokemon_quantity
            )
            if pkmn.is_legendary:
                self.trainer_dao.decrease_legendary_pkmn_count(
                    user_id,
                    quantity
                )
            if pkmn.is_ultra_beast:
                self.trainer_dao.decrease_ultra_beasts_count(
                    user_id,
                    quantity
                )
            if pkmn.is_shiny:
                self.trainer_dao.decrease_shiny_pkmn_count(
                    user_id,
                    quantity
                )
            self.trainer_dao.decrease_total_pkmn_count(
                user_id,
                quantity
            )
            self.trainer_dao.save()
        except HigherReleaseQuantitySpecifiedException:
            raise
        except Exception as e:
            msg = "Error has occurred in deleting pokemon."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def get_egg_count(self, user_id: str) -> int:
        """
        Gets the regular egg count for a user
        """
        try:
            return self.trainer_dao.get_egg_count(user_id)
        except Exception as e:
            msg = "Error has occurred in retrieving egg count."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def decrement_egg_count(self, user_id: str, special_egg: str) -> None:
        """
        Decrements egg count
        """
        try:
            if special_egg == 'm':
                self.trainer_dao.decrement_egg_manaphy_count(user_id)
            else:
                self.trainer_dao.decrement_egg_count(user_id)
        except Exception as e:
            msg = "Error has occurred in decreasing egg count."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def get_egg_manaphy_count(self, user_id: str) -> int:
        """
        Gets the regular egg count for a user
        """
        try:
            return self.trainer_dao.get_egg_manaphy_count(user_id)
        except Exception as e:
            msg = "Error has occurred in retrieving egg manaphy count."
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def get_quantity_of_specified_pokemon(self, user_id: str, pkmn_name: str):
        """
        Gets the quantity of a specified pokemon that the trainer has
        """
        try:
            return self.trainer_dao.get_pokemon_quantity(user_id, pkmn_name)
        except Exception as e:
            msg = ("Error has occurred in getting the quantity of "
                   "specified pokemon")
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def get_lootbox_quantity(self, user_id: str, lootbox: str) -> int:
        """
        Gets the quantity of a specified lootbox from the users inventory
        """
        try:
            if lootbox == self.BRONZE:
                return self.trainer_dao.get_bronze_lootbox_quantity(user_id)
            elif lootbox == self.SILVER:
                return self.trainer_dao.get_silver_lootbox_quantity(user_id)
            elif lootbox == self.GOLD:
                return self.trainer_dao.get_gold_lootbox_quantity(user_id)
            return 0
        except Exception as e:
            msg = ("Error has occurred in getting the quantity of "
                   "specified lootbox")
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise

    def decrement_lootbox_quantity(self, user_id: str, lootbox: str) -> None:
        """
        Decreases the lootbox quantity of a specified lootbox by 1
        """
        try:
            if lootbox == self.BRONZE:
                self.trainer_dao.decrement_bronze_lootbox_quantity(user_id)
            elif lootbox == self.SILVER:
                self.trainer_dao.decrement_silver_lootbox_quantity(user_id)
            elif lootbox == self.GOLD:
                self.trainer_dao.decrement_gold_lootbox_quantity(user_id)
        except Exception as e:
            msg = ("Error has occurred in decrementing the quantity of a"
                   "specified lootbox")
            self.post_error_log_msg(TrainerServiceException.__name__, msg, e)
            raise
