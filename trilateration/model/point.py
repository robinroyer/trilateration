from __future__ import absolute_import

import math
import string

from ..utils.tools import is_number, EARTH_RADIUS

class Point(object):
    """ Representation of a Latitude / Longitude Point"""

    def __init__(self, lat, lon):
        """Point constructor

        Args:
            lat: The latitude value.(-180 < lat < 180)
            lon: The longitude vale.(-90 < lon < 90)
        """
        if not is_number(lon) or lon > 180 or lon < -180:
            raise ValueError("Incorrect longitude" + str(lon))
        if not is_number(lat) or lat > 90 or lat < -90:
            raise ValueError("Incorrect latitude : " + str(lat))
        self.lat = float(lat)
        self.lon = float(lon)

    def __str__(self):
        """Overload __str__ for debug purpose"""
        return "Point ->\n\tlatitude: %f, longitude: %f" % (self.lat, self.lon)

    def to_array(self):
        """export to array"""
        return [self.lat, self.lon]

    def distance_from_point(self, aPoint):
        """
        Calculate the great circle distance between two Points 
        on the earth (specified in decimal degrees)

        Args:
            aPoint: Point to compute the distance from

        Returns:
            great circle distance between the 2 circle center
        """

        if not isinstance(aPoint, Point):
            raise ValueError("Parameter is not a Point")

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(math.radians, [self.lon, self.lat, aPoint.lon, aPoint.lat])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2.)**2. + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2.)**2.
        c = 2. * math.asin(math.sqrt(a))
        return EARTH_RADIUS * c
