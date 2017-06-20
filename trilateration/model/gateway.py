from __future__ import absolute_import

from ..model.point import Point

class Gateway(Point):
    """Represent a Gateway point"""
    def __init__(self, lat, lon, id = "", alt=0):
        """gateway constructor
            see point constructor
        """
        super(Gateway, self).__init__(lat, lon)
        self.id = id
        self.altitude = alt

    # equality overload
    def __eq__(self, other):
        if type(other) is type(self):
            return self.lat == other.lat and self.lon == other.lon and self.altitude == other.altitude
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
