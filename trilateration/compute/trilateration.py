#!/usr/bin/env
# -*- coding:utf-8 -*-

import math
import pyproj
from sympy import Symbol
from sympy.solvers import solve

from trilateration.utils.utils import SPEED_OF_LIGHT
from trilateration.model.point import point
from trilateration.model.circle import circle
from trilateration.model.projection import projection
from trilateration.model.uplink import uplink
from trilateration.model.gateway import gateway

"""
The aim of this lib is to compute the intersection of 3 circles by trilateration.
The 3 circles are defined by a point (lat, long) and a distance(distance or speed * time)

The specific use here is to geolocalise an IOT device from the Date of Arrival of the signal
to 3 gateways.

As we are not in a perfect world, we have imprecission due to the non lign of sight, the timestamp
imprecision and the gateway localisation error. That's why we will never have a perfect intersection of 3 circles.
Instead we will generate a point by approximation, even when we don't have any intersection at all.

Basically we have several cases:
    - one perfect intersection with the 3 circles
    - one area of intersection with the 3 circles
    - intersection between 2 circles and one circle alone
    - no intersection at all

=> we will store the interesting points in the different usecase and generate and return the center of them
   .
  / \
 / ! \   => With no intersection we will consider 2 points that generate the lowest distance between 2 circles
/_____\

"""

class trilateration:
    """This class handle all the trilateration process"""

    def __init__(self, circles_list, projection_system='epsg:2192'):
        """trilateration constructor

        Args:
            circle_list: a List of 3 circle to consider to compute the trilateration
            projection_system: The projection system name to use. (string)
                please choose your projection  http://spatialreference.org/ref/epsg/2192/
        """
        if not isinstance(circles_list, list) or len(circles_list) != 3:
            raise ValueError("Incorrect 3-circle list")
        if not isinstance(projection_system, str):
            raise ValueError("Incorrect projection_system")
        for a_circle in circles_list:
            if not isinstance(a_circle, circle):
                raise ValueError("Invalid item in circles_list is not a circle")

        # PUBLIC
        self.geolocalized_device = None
        self.is_approximation = False

        # PRIVATE
        self._circles = circles_list
        self._level = len(circles_list)
        self._circles_intersections = []
        self._proj = projection(projection_system)
        
        # compute the trilateration
        self._compute_intersections()
        self._compute_geolocalization()


    def _compute_intersections(self):
        """Generate all the intersections between circles (estimated or not)"""
        for i, circle in enumerate(self._circles):
            for j in xrange(i + 1, len(self._circles)):
                inter1, inter2, approximation = circle.intersection_with_circle(self._circles[j], self._proj)
                if inter1 is not None and inter2 is not None:
                    self._circles_intersections.append(inter1)
                    self._circles_intersections.append(inter2)
                if approximation:
                    self.is_approximation = True

    def _compute_geolocalization(self):
        """Generate the mean point corresponding to the device estimated localization"""
        mean_lat, mean_lon = .0, .0
        for intersection in self._circles_intersections:
            mean_lat += intersection.lat
            mean_lon += intersection.lon

        mean_lat /= float(len(self._circles_intersections))
        mean_lon /= float(len(self._circles_intersections))

        self.geolocalized_device = point(mean_lat, mean_lon)


# Test the lib
if __name__ == '__main__':
    c1 = circle(point(48.84, 2.26), 3000)
    c2 = circle(point(48.84, 2.30), 5000)
    c3 = circle(point(48.80, 2.30), 3500)

    trilat = trilateration([c1, c2, c3])
    print trilat.geolocalized_device

