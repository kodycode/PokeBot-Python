from classes import PokeBotModule
from cogs.logic.actions.release_pokemon import ReleasePokemonAction
from modules.pokebot_assets import PokeBotAssets
from modules.pokebot_exceptions import (
    AdminLogicException,
    HigherReleaseQuantitySpecifiedException,
    LootboxDoesNotExistException,
    NotEnoughLootboxQuantityException,
    PokemonDoesNotExistException,
    UnregisteredTrainerException,
)
from modules.pokebot_rates import PokeBotRates
from modules.pokebot_status import PokeBotStatus
from modules.services.trainer_service import TrainerService


class AdminLogic(PokeBotModule):
    """
    Handles logic related to admin command
    """

    # TODO: Keep this value in const file to be used globally
    LOOTBOXES_AVAILABLE = ["bronze", "silver", "gold"]

    def __init__(self, bot):
        self.assets = PokeBotAssets()
        self.rates = PokeBotRates(bot)
        self.status = PokeBotStatus(bot)
        self.trainer_service = TrainerService(self.rates)
        self.release_pokemon = ReleasePokemonAction(
            self.assets,
            self.status,
            self.trainer_service
        )

    async def give_pokemon(
        self,
        user_id: str,
        pkmn_name: str,
        is_shiny=False
    ) -> None:
        """
        Gives a pokemon to the trainer
        """
        try:
            pkmn = self.assets.get_pokemon_asset(pkmn_name, is_shiny)
            self.trainer_service.give_pokemon_to_trainer(
                user_id,
                pkmn,
            )
            self.status.increase_total_pkmn_count(1)
            await self.status.display_total_pokemon_caught()
            self.trainer_service.save_all_trainer_data()
        except PokemonDoesNotExistException:
            raise
        except Exception as e:
            msg = "Error has occurred in giving pokemon to trainer."
            self.post_error_log_msg(AdminLogicException.__name__, msg, e)
            raise

    async def delete_pokemon(
        self,
        user_id: str,
        pkmn_name: str,
    ) -> None:
        """
        Deletes a pokemon from a trainer's inventory
        """
        try:
            self._is_existing_user(user_id)
            await self.release_pokemon.release_pokemon(
                user_id,
                pkmn_name,
                1
            )
        except UnregisteredTrainerException:
            raise
        except HigherReleaseQuantitySpecifiedException:
            raise
        except Exception as e:
            msg = "Error has occurred in deleting trainer's pokemon."
            self.post_error_log_msg(AdminLogicException.__name__, msg, e)
            raise

    async def give_lootbox(
        self,
        user_id: str,
        lootbox: str,
    ) -> None:
        """
        Gives a lootbox to a trainer
        """
        try:
            if lootbox not in self.LOOTBOXES_AVAILABLE:
                raise LootboxDoesNotExistException(lootbox)
            self.trainer_service.give_lootbox_to_trainer(
                user_id,
                lootbox,
            )
            self.trainer_service.save_all_trainer_data()
        except LootboxDoesNotExistException:
            raise
        except Exception as e:
            msg = "Error has occurred in giving a lootbox to a trainer."
            self.post_error_log_msg(AdminLogicException.__name__, msg, e)
            raise

    async def delete_lootbox(
        self,
        user_id: str,
        lootbox: str,
    ) -> None:
        """
        Gives a lootbox to a trainer
        """
        try:
            self._is_existing_user(user_id)
            if lootbox not in self.LOOTBOXES_AVAILABLE:
                raise LootboxDoesNotExistException(lootbox)
            lootbox_quantity = \
                self.trainer_service.get_lootbox_quantity(user_id, lootbox)
            if lootbox_quantity < 1:
                raise NotEnoughLootboxQuantityException(lootbox)
            self.trainer_service.decrement_lootbox_quantity(user_id, lootbox)
            self.trainer_service.save_all_trainer_data()
        except UnregisteredTrainerException:
            raise
        except LootboxDoesNotExistException:
            raise
        except NotEnoughLootboxQuantityException:
            raise
        except Exception as e:
            msg = "Error has occurred in giving a lootbox to a trainer."
            self.post_error_log_msg(AdminLogicException.__name__, msg, e)
            raise

    def _is_existing_user(self, user_id: str) -> None:
        """
        Checks if user exists and throws an UnregisteredTrainerException
        if not
        """
        valid_user = self.trainer_service.check_existing_trainer(user_id)
        if not valid_user:
            raise UnregisteredTrainerException(user_id)
