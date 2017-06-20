from __future__ import absolute_import

import math
import pyproj
from sympy import Symbol
from sympy.solvers import solve

from ..utils.tools import SPEED_OF_LIGHT
from ..model.point import Point
from ..model.circle import Circle
from ..model.projection import Projection

"""
The aim of this lib is to compute the intersection of 3 Circles by Trilateration.
The 3 Circles are defined by a Point (lat, long) and a distance(distance or speed * time)

The specific use here is to geolocalise an IOT device from the Date of Arrival of the signal
to 3 gateways.

As we are not in a perfect world, we have imprecission due to the non lign of sight, the timestamp
imprecision and the gateway localisation error. That's why we will never have a perfect intersection of 3 Circles.
Instead we will generate a Point by approximation, even when we don't have any intersection at all.

Basically we have several cases:
    - one perfect intersection with the 3 Circles
    - one area of intersection with the 3 Circles
    - intersection between 2 Circles and one Circle alone
    - no intersection at all

=> we will store the interesting Points in the different usecase and generate and return the center of them
   .
  / \
 / ! \   => With no intersection we will consider 2 Points that generate the lowest distance between 2 Circles
/_____\

"""

class Trilateration:
    """This class handle all the Trilateration process"""

    def __init__(self, circles_list, projection_system='epsg:2192'):
        """trilateration constructor

        Args:
            Circle_list: a List of 3 Circle to consider to compute the Trilateration
            projection_system: The Projection system name to use. (string)
                please choose your Projection  http://spatialreference.org/ref/epsg/2192/
        """
        if not isinstance(circles_list, list) or len(circles_list) != 3:
            raise ValueError("Incorrect 3-circle list")
        if not isinstance(projection_system, str):
            raise ValueError("Incorrect projection_system")
        for a_circle in circles_list:
            if not isinstance(a_circle, Circle):
                raise ValueError("Invalid item in circles_list is not a Circle")

        # PUBLIC
        self.geolocalized_device = None
        self.is_approximation = False

        # PRIVATE
        self._circles = circles_list
        self._level = len(circles_list)
        self._circles_intersections = []
        self._proj = Projection(projection_system)
        
        # compute the Trilateration
        self._compute_intersections()
        self._compute_geolocalization()


    def _compute_intersections(self):
        """Generate all the intersections between Circles (estimated or not)"""
        for i, Circle in enumerate(self._circles):
            for j in xrange(i + 1, len(self._circles)):
                inter1, inter2, approximation = Circle.intersection_with_circle(self._circles[j], self._proj)
                if inter1 is not None and inter2 is not None:
                    self._circles_intersections.append(inter1)
                    self._circles_intersections.append(inter2)
                if approximation:
                    self.is_approximation = True

    def _compute_geolocalization(self):
        """Generate the mean Point corresponding to the device estimated localization"""
        mean_lat, mean_lon = .0, .0
        for intersection in self._circles_intersections:
            mean_lat += intersection.lat
            mean_lon += intersection.lon

        mean_lat /= float(len(self._circles_intersections))
        mean_lon /= float(len(self._circles_intersections))

        self.geolocalized_device = Point(mean_lat, mean_lon)


# Test the lib
if __name__ == '__main__':
    c1 = Circle(point(48.84, 2.26), 3000)
    c2 = Circle(point(48.84, 2.30), 5000)
    c3 = Circle(point(48.80, 2.30), 3500)

    trilat = Trilateration([c1, c2, c3])
    # print trilat.geolocalized_device

