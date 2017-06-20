from __future__ import absolute_import

import pyproj

class Projection:
    """Check if an object is float, int or long.

    Args:
        object to test

    Returns:
        True if is is as float, int or long, False otherwise

    """

    def __init__(self, a_projection='epsg:2192'):
        """Check if an object is float, int or long.

        Args:
            a_projection string reprentation fo the Projection system
            see http://spatialreference.org/ref/epsg/2192/
        """
        if not isinstance(a_projection, str):
            raise ValueError("The Projection parameter should be a string")
        self.projection = pyproj.Proj(init=a_projection)

    def lat_long_to_x_y(self, lat, lon):
        """
        Transform a latitude, longitude point to as x, y point

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            x, y representation
        """
        return self.projection(lon, lat)

    def x_y_to_long_lat(self, x, y):
        """
        Transform a point x, y to a longitude, latitude point

        Args:
            x: x
            y: y

        Returns:
            Longitude, Latitude representation
        """
        return self.projection(x, y, inverse=True)
