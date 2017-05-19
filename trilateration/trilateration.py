#!/usr/bin/env
# -*- coding:utf-8 -*-

import math
import pyproj
from sympy import Symbol
from sympy.solvers import solve


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

EARTH_RADIUS = 6378100.0

# utils
def is_number(to_test):
    return isinstance(to_test, float) \
        or isinstance(to_test, int) \
        or isinstance(to_test, long)

class projection:
    def __init__(self, a_projection='epsg:2192'):
        self.projection = pyproj.Proj(init=a_projection)

    def lat_long_to_x_y(self, lat, lon):
        """
        Transform a latitude, longitude point to as x, y point

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            (x, y)
        """
        return self.projection(lon, lat)

    def x_y_to_long_lat(self, x, y):
        """
        Transform a point x, y to a longitude, latitude point

        Args:
            x: x
            y: y

        Returns:
            (Longitude, Latitude)
        """
        return self.projection(x, y, inverse=True)


class point:
    """
    Doc
    """

    def __init__(self, lat, lon):
        if not is_number(lon) or lon > 180 or lon < -180:
            raise ValueError("Incorrect longitude")
        if not is_number(lat) or lat > 90 or lat < -90:
            raise ValueError("Incorrect latitude")
        self.lat = float(lat)
        self.lon = float(lon)

    def __str__(self):
        return "Point ->\n\tlatitude: %f, longitude: %f" % (self.lat, self.lon)

    def distance_from_point(self, aPoint):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)

        Args:
            aPoint: Point to compute the distance from

        Returns:
            great circle distance between the 2 circle center
        """

        # if not isinstance(aPoint, point):
        #     return 0 # throw error

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(math.radians, [self.lon, self.lat, aPoint.lon, aPoint.lat])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2.)**2. + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2.)**2.
        c = 2. * math.asin(math.sqrt(a))
        return EARTH_RADIUS * c


class circle:
    """
    Doc
    """
    def __init__(self, a_point, radius):
        if not isinstance(a_point, point):
            raise ValueError("Incorrect point")
        if not is_number(radius) or radius < 0:
            raise ValueError("Incorrect circle radius")
        self.center = a_point
        self.radius = float(radius)

    def __str__(self):
        return "Circle ->\n\tradius: %f\n\tcenter => latitude: %f, longitude: %f" % (self.center.lat, self.center.lon, self.radius)


    def does_intersect(self, a_circle):
        return self.radius + a_circle.radius >= self.center.distance_from_point(a_circle.center)


    def does_contain(self, a_circle):
        return not self.does_intersect(a_circle) and \
        max(self.radius, a_circle.radius) < self.center.distance_from_point(a_circle.center)


    def distance_from_circle_center(self, a_circle):
        """
        return the distance between the center of the 2 circles
        """
        # if not isinstance(a_circle, circle):
        #     return 0 # throw error
        return self.center.distance_from_point(a_circle.center)


    def intersection_with_circle(self, a_circle, proj=projection()):
        """
        return 2 points as intersection of the 2 circles
        the last return parameters shows if there is a real intersection
            or if it is fake intersection points
        """
        # if not isinstance(a_circle, circle):
        #     return point(.0, .0), point(.0, .0) # throw error
        # if self.distance_from_circle_center(a_circle) == 0:
        #     return point(.0, .0), point(.0, .0) # throw error


        # Check if we approximate intersection or not
        approximation = not self.does_intersect(a_circle) or self.does_contain(a_circle)

        #  ============================================================= COMPUTE 
        # projection over x, y
        self_x, self_y = proj.lat_long_to_x_y(self.center.lat, self.center.lon)
        a_circle_x, a_circle_y = proj.lat_long_to_x_y(a_circle.center.lat, a_circle.center.lon)
        # symbole for equation
        x, y = Symbol('x'), Symbol('y')

        equations = []
        equations.append((self_x - x)**2 + (self_y - y)**2  - self.radius**2 )
        equations.append((a_circle_x - x)**2 + (a_circle_y - y)**2  - a_circle.radius**2 )

        res = solve( equations, x, y)

        if not isinstance(res[0], tuple): # no result point
            return None, None, approximation
        elif len(res) == 2:
            lo1, la1 = proj.x_y_to_long_lat(complex(res[0][0]).real, complex(res[0][1]).real)
            lo2, la2 = proj.x_y_to_long_lat(complex(res[1][0]).real, complex(res[1][1]).real)
            return point(la1, lo1), point(la2, lo2), approximation
        else:
            lo1, la1 = proj.x_y_to_long_lat(complex(res[0][0]).real, complex(res[0][1]).real)
            return point(la1, lo1), point(la2, lo2), approximation



class trilateration:
    """
    This class handle all the trilateration process
    please choose your projection  http://spatialreference.org/ref/epsg/2192/
    """

    def __init__(self, circles_list, projection_system='epsg:2192'):
        """
        Doc
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
        """
        generate all the intersections between circles (estimated or not)
        """
        for i, circle in enumerate(self._circles):
            for j in xrange(i + 1, len(self._circles)):
                inter1, inter2, approximation = circle.intersection_with_circle(self._circles[j], self._proj)
                if inter1 is not None and inter2 is not None:
                    self._circles_intersections.append(inter1)
                    self._circles_intersections.append(inter2)
                if approximation:
                    self.is_approximation = True

    def _compute_geolocalization(self):
        """
        Generate the mean point corresponding to the device estimated localization
        """
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

