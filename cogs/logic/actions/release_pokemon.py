from classes import PokeBotModule
from modules.pokebot_assets import PokeBotAssets
from modules.pokebot_status import PokeBotStatus
from modules.pokebot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    ReleasePokemonException,
)
from modules.services import TrainerService
from utils import (
    is_name_shiny,
    remove_shiny_pokemon_name,
)


class ReleasePokemonAction(PokeBotModule):
    """
    Handles the actions for releasing pokemon
    """
    def __init__(
        self, assets: PokeBotAssets,
        status: PokeBotStatus,
        trainer_service: TrainerService
    ):
        self.assets = assets
        self.status = status
        self.trainer_service = trainer_service

    async def release_pokemon(
        self,
        user_id: str,
        pkmn_name: str,
        quantity: int
    ) -> None:
        """
        Deletes a pokemon from the trainer's inventory
        """
        try:
            await self._process_pokemon_release(user_id, pkmn_name, quantity)
            self.trainer_service.save_all_trainer_data()
            self.status.decrease_total_pkmn_count(1)
            await self.status.display_total_pokemon_caught()
        except HigherReleaseQuantitySpecifiedException:
            raise
        except Exception as e:
            msg = "Error has occurred in releasing pokemon."
            self.post_error_log_msg(ReleasePokemonException.__name__, msg, e)
            raise

    async def _process_pokemon_release(
        self,
        user_id: str,
        pkmn_name: str,
        quantity: int
    ):
        """
        Processes pokemon to release
        """
        try:
            pkmn_lowercase = pkmn_name.lower()
            is_shiny = is_name_shiny(pkmn_lowercase)
            no_shiny_pkmn_name = remove_shiny_pokemon_name(pkmn_lowercase)
            pkmn = self.assets.get_pokemon_asset(
                no_shiny_pkmn_name,
                is_shiny=is_shiny
            )   
            await self.trainer_service.decrease_pokemon_quantity(
                user_id,
                pkmn,
                quantity
            )
        except Exception as e:
            raise
