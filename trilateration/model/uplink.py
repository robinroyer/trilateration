
from gateway import gateway
from utils.utils import is_number

class uplink:
    """Represent a message arrived at a datetime at a certain nanosecond time"""

    def __init__(self, a_gateway, date, timestamp):
        """Uplink constructor

        Args:
            a_gateway: the gateway that has received the message
            date: the date of the message
            timestamp: a precised time (nanosecond) for calculous
        """
        if not isinstance(a_gateway, gateway):
            raise ValueError("Incorrect point")
        if not is_number(timestamp) or timestamp < 0:
            raise ValueError("Incorrect timestamp")
        self.gateway = a_gateway
        self.arrival_date = date
        self.timestamp = timestamp

