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
        self.lat = lat
        self.lon = lon

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

        if not isinstance(aPoint, point):
            return 0 # throw error

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
    def __init__(self, point, radius):
        self.center = point
        self.radius = radius

    def __str__(self):
        return "Circle ->\n\tradius: %f\n\tcenter => latitude: %f, longitude: %f" % (self.center.lat, self.center.lon, self.radius)

    def distance_from_circle_center(self, a_circle):
        """
        return the distance between the center of the 2 circles
        """
        if not isinstance(a_circle, circle):
            return 0 # throw error
        return 0#self.center.distance_from_point(a_circle.center)


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

        distance = self.distance_from_circle_center(a_circle)
        # check circle condition
        does_intersect = self.radius + a_circle.radius >= distance
        does_contain = not does_intersect and max(self.radius, a_circle.radius) < distance

        print does_intersect
        print does_contain


        if does_intersect and not does_contain:
            # projection over x, y
            self_x, self_y = proj.lat_long_to_x_y(self.center.lat, self.center.lon)
            a_circle_x, a_circle_y = proj.lat_long_to_x_y(a_circle.center.lat, a_circle.center.lon)
            # compute intersections
            x, y = Symbol('x'), Symbol('y')

            equations = []
            equations.append((self_x - x)**2 + (self_y - y)**2  - self.radius**2 )
            equations.append((a_circle_x - x)**2 + (a_circle_y - y)**2  - a_circle.radius**2 )

            res = solve( equations, x, y)

            print res
            return point(.0, .0), point(.0, .0)
            pass
        else: # one circle contain the other or they are too far away from each other
            self.is_approximation = True
            # generate fake intersections
            return point(.0, .0), point(.0, .0)


class trilateration:
    """
    This class handle all the trilateration process
    # please choose tour projection  http://spatialreference.org/ref/epsg/2192/
    """

    def __init__(self, circles_list, projection_system='epsg:2192'):
        """
        Doc
        """
        # PUBLIC
        self.geolocalized_device = None
        self.is_approximation = False

        # PRIVATE
        self.__circles = circles_list
        self.__level = len(circles_list)
        self.__circles_intersections = []
        self.__proj = projection(projection_system)
        
        # compute the trilateration
        self.__compute_intersections()
        self.__compute_geolocalization()


    def __compute_intersections(self):
        """
        generate all the intersections between circles (estimated or not)
        """
        if self.__level == 0:
            return 0 # throw error -> we are no magicians
        if self.__level == 1:
            return 0 # throw error -> we are no magicians
        if self.__level == 2:
            return 0 # throw error -> we are no magicians

        for i, circle in enumerate(self.__circles):
            for j in xrange(i + 1, len(self.__circles)):
                inter1, inter2 = circle.intersection_with_circle(self.__circles[j], self.__proj)
                self.__circles_intersections.append(inter1)
                self.__circles_intersections.append(inter2)

    def __compute_geolocalization(self):
        """
        Generate the mean point corresponding to the device estimated localization
        """
        mean_lat, mean_lon = .0, .0
        for intersection in self.__circles_intersections:
            mean_lat += intersection.lat
            mean_lon += intersection.lon

        mean_lat /= float(len(self.__circles_intersections))
        mean_lon /= float(len(self.__circles_intersections))

        self.geolocalized_device = point(mean_lat, mean_lon)




# Test the lib
if __name__ == '__main__':

    c1 = circle(point(0,0), 1)
    c2 = circle(point(2,0), 1)
    c3 = circle(point(1,1), 1)

    trilat = trilateration([c1, c2, c3])




