from classes import PokeBotEvent
from collections import defaultdict


class NightVendorEvent(PokeBotEvent):
    def __init__(self, bot):
        super().__init__(bot, "night_vendor_event")
        self.roll_counts = {}
        self.offers = {}
        self.sales = set()

    async def activate(self):
        """
        Activates night vendor event
        """
        if not self.is_active:
            self.is_active = True
            msg = ("**The Night Vendor has arrived! Use the `{0}vendor i` "
                "command for info on what's he's trading. If you're "
                "interested in the trade, type `{0}vendor t` to make. "
                "the trade. If you don't like the roll, type `{0}vendor r` "
                "to re-roll what the vendor has for sale.**"
                "".format(self.bot.command_prefix))
            await self._send_event_start_msg(msg)

    async def deactivate(self):
        """
        Deactivates night vendor event
        """
        self.night_vendor = False
        msg = ("**The night vendor has vanished.**")
        await self._send_event_end_msg(msg)

    def check_user_has_offer(self, user_id: str) -> bool:
        """
        Checks if the user has an offer from the night vendor
        """
        if user_id in self.offers:
            return True
        return False

    def get_reroll_count(self) -> int:
        """
        Gets the shiny rate modifier of a night vendor roll
        """
        return self.event_data["reroll_count"]

    def get_shiny_roll_rate_modifier(self) -> int:
        """
        Gets the shiny rate modifier of a night vendor roll
        """
        return self.event_data["shiny_roll_rate_modifier"]

    def get_night_vendor_offered_pokemon(self, user_id: str) -> str:
        """
        Gets the offered pokemon from the night vendor
        """
        return self.offers[user_id]["offer"]["pkmn"]

    def get_night_vendor_requested_pokemon(self, user_id: str) -> str:
        """
        Gets the night vendor's requested pokemon
        """
        return self.offers[user_id]["price"]

    def get_night_vendor_offered_pokemon_shiny_status(
        self,
        user_id: str
    ) -> str:
        """
        Gets the shiny status of the offered pokemon from the night vendor
        """
        return self.offers[user_id]["offer"]["is_shiny"]

    def get_trainer_roll_count(self, user_id: str) -> int:
        """
        Gets the roll count of a trainer
        """
        return self.roll_counts[user_id]

    def update_night_vendor_offer(
        self,
        user_id: str,
        night_vendor_offer: dict
    ) -> None:
        """
        Updates the night vendor offer to a trainer in the
        dict of offers
        """
        self.offers[user_id] = night_vendor_offer

    def update_night_vendor_sales(
        self,
        user_id: str
    ) -> None:
        """
        Updates the list of sales that were completed with the night vendor
        """
        self.sales.add(user_id)

    def create_or_update_roll_count(self, user_id: str):
        """
        Creates or updates the count of rolls for a trainer
        """
        if user_id not in self.roll_counts:
            self.roll_counts = self.event.get_reroll_count()
        else:
            self.roll_counts -= 1


