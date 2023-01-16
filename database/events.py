from classes import DataDAO


EVENTS_JSON_NAME = "events.json"


class EventsDAO(DataDAO):
    """
    Gets the list of events that are available
    """
    def __init__(self, filename=EVENTS_JSON_NAME):
        super().__init__(filename)
        

    def get_events(self) -> dict:
        """
        Gets the list of events that are available
        """
        return self.data

