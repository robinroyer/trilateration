#!/usr/bin/env
# -*- coding:utf-8 -*-
from __future__ import absolute_import

import time
import string
import pyproj
import datetime
import numpy as np
from sympy import Symbol, sqrt, Eq, Abs
from sympy.solvers import solve

from ..utils.tools import SPEED_OF_LIGHT
from ..model.point import Point
from ..model.projection import Projection
from ..model.uplink import Uplink
from ..model.gateway import Gateway

"""
The aim of this lib is to compute the geolocalization of a device by the time of arrival at 3 Gateways.

=> we will store the interesting Points in the different usecase and generate and return the center of them
   .
  / \
 / ! \   => We can not compute the response if we have the same Gateway twice
/_____\

"""
class Toa:
    """This class handle all the Toa process"""

    def __init__(self, uplink_list, projection_system='epsg:2192'):
        """toa constructor

        Args:
            uplink_list: a List of 3 circle to consider to compute the trilateration
            projection_system: The Projection system name to use. (string)
                please choose your Projection  http://spatialreference.org/ref/epsg/2192/
        """
        if not isinstance(uplink_list, list) and not isinstance(uplink_list, np.ndarray)  or len(uplink_list) != 3:
            raise ValueError("Incorrect uplink_list is not a list")
        if not isinstance(projection_system, str):
            raise ValueError("Incorrect projection_system")
        for uplk in uplink_list:
            if not isinstance(uplk, Uplink):
                raise ValueError("Invalid item in uplink_list is not a Uplink")

        # PUBLIC
        self.geolocalized_device = Point(.0, .0)
        self.is_resolved = False

        # PRIVATE
        self._uplinks = uplink_list
        self._level = len(uplink_list)
        self._equations = []
        self._intersections = []
        self._proj = Projection(projection_system)
        
        # compute the trilateration
        self._compute_intersections()
        self._compute_geolocalization()


    def _compute_intersections(self):
        """Generate all the intersections between circles (estimated or not)
            v * (ti - tj) = ((Xi - x) ** 2 + (Yi - y) ** 2 ^ 1/2 
                          - ((Xj - x) ** 2 + (Yj - y) ** 2 ^ 1/2
        """
        x, y = Symbol('x'), Symbol('y')

        # generate all the equations
        for i, uplink in enumerate(self._uplinks):
            for j in xrange(i + 1, len(self._uplinks)):
                # Projection over x, y
                gw_x, gw_y = self._proj.lat_long_to_x_y(uplink.gateway.lat, uplink.gateway.lon)
                a_gw_x, a_gw_y = self._proj.lat_long_to_x_y(self._uplinks[j].gateway.lat, self._uplinks[j].gateway.lon)
                gw_ts, a_gw_ts = uplink.timestamp, self._uplinks[j].timestamp

                self._equations.append( sqrt((gw_x - x)**2 + (gw_y - y)**2) - sqrt((a_gw_x - x)**2 + (a_gw_y - y)**2) \
                     - Abs(SPEED_OF_LIGHT * (gw_ts - a_gw_ts) ))

        solutions = []
        for i, equation in enumerate(self._equations):
            for j in xrange(i + 1, len(self._equations)):
                solutions.append(solve([self._equations[i], self._equations[j]]))
        # generate intersection Points
        for solution in solutions:
            try:
                # print solution[0]
                lon, lat = self._proj.x_y_to_long_lat(solution[0][x], solution[0][y])
                self._intersections.append(Point(lat, lon))
            except Exception as e:
                #  TODO:should log
                # print e
                pass


    def _compute_geolocalization(self):
        """Generate the mean Point corresponding to the device estimated localization"""
        if len(self._intersections) == 0:
            return
        mean_lat, mean_lon = .0, .0
        for intersection in self._intersections:
            mean_lat += intersection.lat
            mean_lon += intersection.lon

        mean_lat /= float(len(self._intersections))
        mean_lon /= float(len(self._intersections))

        self.is_resolved = True
        self.geolocalized_device = Point(mean_lat, mean_lon)


# Test the lib
if __name__ == '__main__':
    g1 = Gateway(48.84, 2.26)
    g2 = Gateway(48.84, 2.30)
    g3 = Gateway(48.80, 2.30)

    t1 = int(time.time() * 1000000000)
    t2 = int(time.time() * 1000000000)
    t3 = int(time.time() * 1000000000)    

    u1 = Uplink(g1, datetime.datetime.now(), t1)
    u2 = Uplink(g2, datetime.datetime.now(), t2)
    u3 = Uplink(g3, datetime.datetime.now(), t3)

    solver = Toa([u1, u2, u3])
    # print solver.geolocalized_device

