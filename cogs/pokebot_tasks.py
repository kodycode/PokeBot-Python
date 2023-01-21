from bot_logger import logger
from modules import PokeBotCog
import datetime
import asyncio


class PokeBotTasks(PokeBotCog):
    """Runs async tasks for PokeBot that run in a timely manner"""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    #     self.bot.loop.create_task(self._update_cache())
    #     self.bot.loop.create_task(self._load_event())
    #     self.bot.loop.create_task(self._refresh_daily())

    # async def _update_cache(self):
    #     """
    #     Calls function to cache user objects every hour
    #     """
    #     while True:
    #         await self._cache_users()
    #         await asyncio.sleep(3600)

    # async def _cache_users(self):
    #     """
    #     Caches user data based on the trainers in trainers.json
    #     """
    #     try:
    #         trainer_cache = {}
    #         for trainer in self.trainer_data:
    #             user_obj = await self.bot.fetch_user(str(trainer))
    #             trainer_cache[trainer] = user_obj
    #         self.trainer_cache = trainer_cache
    #     except Exception as e:
    #         print("Failed to cache trainer object. See error.log.")
    #         logger.error("Exception: {}".format(str(e)))

    # async def _load_event(self):
    #     """
    #     Checks if it's time for an event and activates it if it is
    #     """
    #     while True:
    #         hour = int(datetime.datetime.now().hour)
    #         happy_hour_event = self.event.happy_hour_event_data
    #         night_vendor_event = self.event.night_vendor_event_data
    #         if happy_hour_event["event"]:
    #             if hour == happy_hour_event["event_start_hour"]:
    #                 await self.event.activate_happy_hour()
    #                 await asyncio.sleep(happy_hour_event["duration"])
    #                 await self.event.deactivate_happy_hour()
    #         if night_vendor_event["event"]:
    #             if hour == night_vendor_event["event_start_hour"]:
    #                 reroll_count = night_vendor_event["reroll_count"]
    #                 for trainer in self.trainer_data:
    #                     trainer_profile = self.trainer_data[trainer]
    #                     trainer_profile["reroll_count"] = reroll_count
    #                 self._save_trainer_file(self.trainer_data)
    #                 await self.event.activate_night_vendor()
    #                 await asyncio.sleep(night_vendor_event["duration"])
    #                 await self.event.deactivate_night_vendor()
    #                 self.vendor_sales.clear()
    #                 self.vendor_trade_list.clear()
    #         await asyncio.sleep(60)

    # async def _refresh_daily(self):
    #     """
    #     Checks and refreshes the daily
    #     """
    #     while True:
    #         hour = int(datetime.datetime.now().hour)
    #         if hour == self.config_data["daily_reset_hour"]:
    #             self._save_daily_file([])
    #             self.daily_data = self._load_daily_file()
    #             await asyncio.sleep(3600)
    #         await asyncio.sleep(60)
