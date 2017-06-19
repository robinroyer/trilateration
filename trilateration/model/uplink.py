from __future__ import absolute_import

from ..utils.tools import is_number
from ..model.gateway import Gateway

class Uplink:
    """Represent a message arrived at a datetime at a certain nanosecond time"""

    def __init__(self, a_gateway, date, timestamp):
        """Uplink constructor

        Args:
            a_gateway: the gateway that has received the message
            date: the date of the message
            timestamp: a precised time (nanosecond) for calculous
        """
        if not isinstance(a_gateway, Gateway):
            raise ValueError("Incorrect point")
        if not is_number(timestamp) or timestamp < 0:
            raise ValueError("Incorrect timestamp")
        self.gateway = a_gateway
        self.arrival_date = date
        self.timestamp = timestamp

