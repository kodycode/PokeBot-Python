from classes import PokeBotModule
from cogs.logic.actions.release_pokemon import ReleasePokemonAction
from events.night_vendor_event import NightVendorEvent
from modules.pokebot_exceptions import (
    HigherReleaseQuantitySpecifiedException,
    NightVendorLogicException,
    NightVendorSaleAlreadyMadeException,
    NotEnoughRerollsException,
    UnavailablePokemonToTradeException
)
from modules.pokebot_assets import PokeBotAssets
from modules.pokebot_generator import PokeBotGenerator
from modules.pokebot_rates import PokeBotRates
from modules.pokebot_status import PokeBotStatus
from modules.services.trainer_service import TrainerService
from utils import get_ctx_user_id
import discord


class NightVendorLogic(PokeBotModule):
    """Handles the night vendor logic of features for PokeBot"""

    def __init__(self, bot, event: NightVendorEvent):
        self.assets = PokeBotAssets()
        self.event = event
        self.rates = PokeBotRates(bot)
        self.status = PokeBotStatus(bot)
        self.generator = PokeBotGenerator(self.assets, self.rates)
        self.trainer_service = TrainerService(self.rates)
        self.release_pokemon_action = ReleasePokemonAction(
            self.assets,
            self.status,
            self.trainer_service,
        )

    def build_night_vendor_offer_msg(
        self,
        ctx: discord.ext.commands.Context
    ) -> str:
        """
        Builds the message for the night vendor offer
        """
        try:
            user_id = get_ctx_user_id(ctx)
            if self.event.check_user_traded(user_id):
                raise NightVendorSaleAlreadyMadeException()
            if not self.event.check_user_has_offer(user_id):
                self.event.create_or_update_roll_count(user_id)
                self._create_night_vendor_offer(user_id)
            night_vendor_pkmn = self.event.get_night_vendor_offered_pokemon(
                user_id
            )
            if self.event.get_night_vendor_offered_pokemon_shiny_status(
                user_id
            ):
                night_vendor_pkmn = "(Shiny) " + night_vendor_pkmn
            night_vendor_price = self.event.get_night_vendor_requested_pokemon(
                user_id
            )
            msg = (f"{ctx.message.author.mention},"
                   " the **Night Vendor**"
                   " wants to trade their **{}** for a **{}**"
                   "".format(
                    night_vendor_pkmn.title(),
                    night_vendor_price.title()
                    )
                )
            return msg
        except NightVendorSaleAlreadyMadeException:
            raise
        except Exception as e:
            msg = "Error has occurred in building night vendor offer msg."
            self.post_error_log_msg(NightVendorLogicException.__name__, msg, e)
            raise
    
    def _create_night_vendor_offer(self, user_id: str):
        """
        Creates an offer from the night vendor to trade
        """
        try:
            offer_pkmn = self.generator.generate_random_pokemon(
                is_night_vendor_generated=True
            )
            random_pokemon_req = self.generator.generate_random_pokemon()
            night_vendor_offer = {
                "offer": {
                    "pkmn": offer_pkmn.name,
                    "is_shiny": offer_pkmn.is_shiny
                },
                "price": random_pokemon_req.name
            }
            self.event.update_night_vendor_offer(user_id, night_vendor_offer)
        except Exception as e:
            msg = "Error has occurred in creating night vendor offer."
            self.post_error_log_msg(NightVendorLogicException.__name__, msg, e)
            raise
        
    def reroll_night_vendor_offer(
        self,
        ctx: discord.ext.commands.Context
    ) -> None:
        """
        Rerolls what the night vendor has to offer to the trainer
        """
        try:
            user_id = get_ctx_user_id(ctx)
            if self.event.check_user_traded(user_id):
                raise NightVendorSaleAlreadyMadeException()
            roll_count = self.event.get_trainer_roll_count(user_id)
            if roll_count < 1:
                raise NotEnoughRerollsException()
            self.event.create_or_update_roll_count(user_id)
            self._create_night_vendor_offer(user_id)
        except NightVendorSaleAlreadyMadeException:
            raise
        except NotEnoughRerollsException:
            raise
        except Exception as e:
            msg = "Error has occurred in rerolling night vendor offer msg."
            self.post_error_log_msg(NightVendorLogicException.__name__, msg, e)
            raise

    async def trade_night_vendor(
        self,
        ctx: discord.ext.commands.Context
    ) -> str:
        """
        Trades and the night vendor
        """
        try:
            user_id = get_ctx_user_id(ctx)
            if not self.event.check_user_has_offer(user_id):
                self.event.create_or_update_roll_count(user_id)
                self._create_night_vendor_offer(user_id)
            if self.event.check_user_traded(user_id):
                raise NightVendorSaleAlreadyMadeException()
            night_vendor_pkmn_name = self.event.get_night_vendor_offered_pokemon(
                user_id
            )
            is_night_vendor_pkmn_shiny = self.event.get_night_vendor_offered_pokemon_shiny_status(user_id)
            night_vendor_pkmn = self.assets.get_pokemon_asset(
                night_vendor_pkmn_name,
                is_night_vendor_pkmn_shiny
            )
            night_vendor_price = self.event.get_night_vendor_requested_pokemon(
                user_id
            )
            try:
                await self.release_pokemon_action.release_pokemon(
                    user_id,
                    night_vendor_price,
                    1
                )
            except HigherReleaseQuantitySpecifiedException:
                raise UnavailablePokemonToTradeException(
                    night_vendor_price
                )
            self.trainer_service.give_pokemon_to_trainer(
                user_id,
                night_vendor_pkmn
            )
            self.trainer_service.save_all_trainer_data()
            self.event.update_night_vendor_sales(user_id)
            formatted_offered_pkmn_name = night_vendor_pkmn.name.title()
            if is_night_vendor_pkmn_shiny:
                formatted_offered_pkmn_name = \
                    "(Shiny) " + formatted_offered_pkmn_name
            formatted_price_pkmn_name = night_vendor_price.title()
            msg = (f"{ctx.message.author.mention} traded a"
                   f" **{formatted_offered_pkmn_name}** for a"
                   f" **{formatted_price_pkmn_name}**!")
            return msg
        except NightVendorSaleAlreadyMadeException:
            raise
        except UnavailablePokemonToTradeException:
            raise
        except Exception as e:
            msg = "Error has occurred in trading with the night vendor."
            self.post_error_log_msg(NightVendorLogicException.__name__, msg, e)
            raise
