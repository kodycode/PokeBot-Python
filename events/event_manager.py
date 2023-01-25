from events.happy_hour_event import HappyHourEvent
from events.night_vendor_event import NightVendorEvent
import datetime


class EventManager(object):
    def __init__(self, bot):
        if(self.__initialized): return
        self.__initialized = True
        self.active_events = {}
        self.events = [
            HappyHourEvent(bot),
            NightVendorEvent(bot),
        ]
        self.event_catch_cooldown_modifier = 1.0
        self.event_shiny_catch_rate_modifier = 1.0

    def __new__(*args):
        cls = args[0]
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventManager, cls).__new__(cls)
            cls.instance.__initialized = False
            return cls.instance
        return cls.instance

    def _get_all_events(self) -> list:
        return self.events

    def get_event_catch_cooldown_modifier(self) -> float:
        return self.event_catch_cooldown_modifier

    def get_event_shiny_catch_rate_modifier(self) -> float:
        return self.event_shiny_catch_rate_modifier

    async def process_all_event_activation_times(self) -> None:
        """
        Iterate through each event to determine activation and
        apply side effects
        """
        hour = int(datetime.datetime.now().hour)
        for event in self.events:
            await event.process_event_activation_time(hour)
            await self._set_event_side_effects(event)

    async def _set_event_side_effects(self, event) -> None:
        """
        Sets the side effects that occur from active/inactive events
        """
        if event.is_active:
            if type(event).__name__ not in self.active_events:
                self.active_events[type(event).__name__] = True
                self.event_catch_cooldown_modifier *= event.catch_cooldown_modifier
                self.event_shiny_catch_rate_modifier *= event.shiny_catch_rate_modifier
        else:
            if type(event).__name__ in self.active_events:
                self.active_events[type(event).__name__] = False
                self.event_catch_cooldown_modifier /= event.catch_cooldown_modifier
                self.event_shiny_catch_rate_modifier /= event.shiny_catch_rate_modifier
