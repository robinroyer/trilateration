#!/usr/bin/env
# -*- coding:utf-8 -*-

import time
import string
import math
import pyproj
import datetime
import numpy as np
from sympy import Symbol, sqrt, Eq, Abs
from sympy.solvers import solve
from sympy import linsolve
from scipy.optimize import least_squares

from ..utils.utils import SPEED_OF_LIGHT
from ..model.point import point
from ..model.projection import projection
from ..model.uplink import uplink
from ..model.gateway import gateway

"""
The aim of this lib is to compute the geolocalization of a device by the time difference of arrival at 3 gateways.

=> we will store the interesting points in the different usecases and return the center of them
   .
  / \
 / ! \   => We can not compute the response if we have the same gateway twice
/_____\

"""
class lsm:
    """This class handle all the tdoa process"""

    def __init__(self, uplink_list, projection_system='epsg:2192'):
        """tdoa constructor

        Args:
            uplink_list: a List of 4 uplinks to consider to compute the tdoa
            projection_system: The projection system name to use. (string)
                please choose your projection  http://spatialreference.org/ref/epsg/2192/
        """
        if not isinstance(uplink_list, list) and not isinstance(uplink_list, np.ndarray)  or len(uplink_list) < 3:
            raise ValueError("Incorrect uplink_list is not a list or not enough uplink" + str(type(uplink_list)) )
        if not isinstance(projection_system, str):
            raise ValueError("Incorrect projection_system")
        for uplk in uplink_list:
            if not isinstance(uplk, uplink):
                raise ValueError("Invalid item in uplink_list is not a uplink :")
        #check gateway uniqueness
        for i, uplk in enumerate(uplink_list):
            for j in xrange(i+1, len(uplink_list)):
                if uplink_list[i].gateway == uplink_list[j].gateway:
                    raise ValueError("Gateway is not unique")

        # PUBLIC
        self.geolocalized_device = point(.0, .0)
        self.is_resolved = False

        # PRIVATE
        self._uplinks = uplink_list
        self._level = len(uplink_list)
        self._equations = []
        self._intersections = []
        self._proj = projection(projection_system)
        
        # compute the trilateration
        self._compute_geolocalization()

    def _lsm_loss_clojure(self):
        """
        Algorithm:
        The goal is to resolve the equation:with a least 4 gatreways (2, 3, 4)
        x * Am + y * Bm + z * Cm + Dm = 0   
            => mat A * mat X = - mat B

        with:
            Am = (2 * Xm) / (v * Tm) - (2 * X1) / (v * T1)
            Bm = (2 * Ym) / (v * Tm) - (2 * Y1) / (v * T1)
            Cm = (2 * Zm) / (v * Tm) - (2 * Z1) / (v * T1)
            Dm = v * Tm - v * T1 - (Xm * Xm + Ym * Ym + Zm * Zm) / (v * Tm) + (X1 * X1 + Y1 * Y1 + Z1 * Z1) / (v * T1)

            As we don't have informations about the Z value, we will compute as if z = 0

            =>
                Am = (2 * Xm) / (v * Tm) - (2 * X1) / (v * T1)
                Bm = (2 * Ym) / (v * Tm) - (2 * Y1) / (v * T1)
                Dm = v * Tm - v * T1 - (Xm * Xm + Ym * Ym) / (v * Tm) + (X1 * X1 + Y1 * Y1) / (v * T1)
        """
        # Pivot values
        x0, y0 = self._proj.lat_long_to_x_y(self._uplinks[0].gateway.lat, self._uplinks[0].gateway.lon)
        t0 = self._uplinks[0].timestamp

        def clojure(x):
            loss = .0
            for i, uplink in enumerate(self._uplinks):
                if i == 0:
                    continue
                gw_x, gw_y = self._proj.lat_long_to_x_y(uplink.gateway.lat, uplink.gateway.lon)
                gw_ts = uplink.timestamp

                loss += abs(math.sqrt((gw_x - x[0])**2 + (gw_y - x[1])**2) - math.sqrt((x0 - x[0])**2 + (y0 - x[1])**2) - SPEED_OF_LIGHT * (gw_ts - t0))
                return loss
        return clojure

    def _compute_geolocalization(self):
        x0, y0 = self._proj.lat_long_to_x_y(self._uplinks[0].gateway.lat, self._uplinks[0].gateway.lon)
        solution = least_squares(self._lsm_loss_clojure(), [x0, y0])
        lon, lat = self._proj.x_y_to_long_lat(solution["x"][0], solution["x"][1])
        self.is_resolved = True
        self.geolocalized_device = point(lat, lon)


# Test the lib
if __name__ == '__main__':
    g1 = gateway(48.84, 2.26)
    g2 = gateway(48.84, 2.30)
    g3 = gateway(48.80, 2.33)
    g4 = gateway(48.90, 2.40)
    g5 = gateway(48.90, 2.50)

    t1 = int(time.time() * 1000000000)
    t2 = int(time.time() * 1000000000)
    t3 = int(time.time() * 1000000000)    
    t4 = int(time.time() * 1000000000)
    t5 = int(time.time() * 1000000000)

    u1 = uplink(g1, datetime.datetime.now(), t1)
    u2 = uplink(g2, datetime.datetime.now(), t2)
    u3 = uplink(g3, datetime.datetime.now(), t3)
    u4 = uplink(g4, datetime.datetime.now(), t4)
    u5 = uplink(g5, datetime.datetime.now(), t4)

    solver = lsm([u1, u2, u3, u4, u5])
    print solver.geolocalized_device

