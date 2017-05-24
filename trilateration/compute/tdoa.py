#!/usr/bin/env
# -*- coding:utf-8 -*-

import time
import pyproj
import datetime
from sympy import Symbol, sqrt, Eq, Abs
from sympy.solvers import solve
from sympy import linsolve

from utils.utils import SPEED_OF_LIGHT
from model.point import point
from model.projection import projection
from model.uplink import uplink
from model.gateway import gateway

"""
The aim of this lib is to compute the geolocalization of a device by the time difference of arrival at 3 gateways.

=> we will store the interesting points in the different usecases and return the center of them
   .
  / \
 / ! \   => We can not compute the response if we have the same gateway twice
/_____\

"""
class tdoa:
    """This class handle all the tdoa process"""

    def __init__(self, uplink_list, projection_system='epsg:2192'):
        """tdoa constructor

        Args:
            uplink_list: a List of 4 uplinks to consider to compute the tdoa
            projection_system: The projection system name to use. (string)
                please choose your projection  http://spatialreference.org/ref/epsg/2192/
        """
        if not isinstance(uplink_list, list) or len(uplink_list) != 4:
            raise ValueError("Incorrect uplink_list is not a list")
        if not isinstance(projection_system, str):
            raise ValueError("Incorrect projection_system")
        for uplk in uplink_list:
            if not isinstance(uplk, uplink):
                raise ValueError("Invalid item in uplink_list is not a uplink")
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
        self._compute_intersections()
        self._compute_geolocalization()


    def _compute_intersections(self):
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
        x, y = Symbol('x'), Symbol('y')

        # Pivot values
        x0, y0 = self._proj.lat_long_to_x_y(self._uplinks[0].gateway.lat, self._uplinks[0].gateway.lon)
        t0 = self._uplinks[0].timestamp

        # delta 1
        x1, y1 = self._proj.lat_long_to_x_y(self._uplinks[1].gateway.lat, self._uplinks[1].gateway.lon)
        t1 = self._uplinks[1].timestamp
        dx1, dy1, dt1 = x1 - x0, y1 - y0, t1 - t0

        for i in xrange(2, len(self._uplinks)):
            # delta n
            gw_x, gw_y = self._proj.lat_long_to_x_y(self._uplinks[i].gateway.lat, self._uplinks[i].gateway.lon)
            gw_ts = self._uplinks[i].timestamp
            dxn, dyn, dtn = gw_x - x0, gw_y - y0, gw_ts - t0

            # algorithm explained previously
            A = (2 * dxn / SPEED_OF_LIGHT * dtn) - (2 * dx1 / SPEED_OF_LIGHT * dt1)
            B = (2 * dyn / SPEED_OF_LIGHT * dtn) - (2 * dy1 / SPEED_OF_LIGHT * dt1)
            D = SPEED_OF_LIGHT * (dtn - dt1) - ((dxn**2 + dyn**2) / SPEED_OF_LIGHT * dtn) + ((dx1**2 + dy1**2) / SPEED_OF_LIGHT * dt1)
            self._equations.append( A * x + B * y + D )

        solution = list(linsolve(self._equations, (x,y)))
        lon, lat = self._proj.x_y_to_long_lat(x0 + solution[0][0], y0 + solution[0][1])
        self._intersections.append(point(lat, lon))


    def _compute_geolocalization(self):
        """Generate the mean point corresponding to the device estimated localization"""
        if len(self._intersections) == 0:
            return
        mean_lat, mean_lon = .0, .0
        for intersection in self._intersections:
            mean_lat += intersection.lat
            mean_lon += intersection.lon

        mean_lat /= float(len(self._intersections))
        mean_lon /= float(len(self._intersections))

        self.is_resolved = True
        self.geolocalized_device = point(mean_lat, mean_lon)


# Test the lib
if __name__ == '__main__':
    g1 = gateway(48.84, 2.26)
    g2 = gateway(48.84, 2.30)
    g3 = gateway(48.80, 2.30)
    g4 = gateway(48.90, 2.40)

    t1 = int(time.time() * 1000000000)
    t2 = int(time.time() * 1000000000)
    t3 = int(time.time() * 1000000000)    
    t4 = int(time.time() * 1000000000)

    u1 = uplink(g1, datetime.datetime.now(), t1)
    u2 = uplink(g2, datetime.datetime.now(), t2)
    u3 = uplink(g3, datetime.datetime.now(), t3)
    u4 = uplink(g4, datetime.datetime.now(), t4)

    solver = tdoa([u1, u2, u3, u4])
    print solver.geolocalized_device

