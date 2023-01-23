from classes import DataDAO


EVENTS_JSON_NAME = "events.json"


class EventsDAO(DataDAO):
    """
    Gets the list of events that are available
    """
    def __init__(self, filename=EVENTS_JSON_NAME):
        super().__init__(filename)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventsDAO, cls).__new__(cls)
            return cls.instance
        return cls.instance

    def get_events(self) -> dict:
        """
        Gets the list of events that are available
        """
        return self.data

    def get_event(self, event_key: str) -> dict:
        """
        Gets the specific event data using the event key
        """
        return self.data[event_key]
