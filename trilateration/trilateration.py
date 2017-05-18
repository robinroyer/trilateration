#!/usr/bin/env
# -*- coding:utf-8 -*-

import math

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



class point(object):
    """
    Doc
    """

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def distance_from_point(aPoint):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)

        Args:
            lat1: Latitude of the 1st point
            lon1: Longitude of the 1st point
            lat2: Latitude of the 2nd point
            lon2: Longitude of the 2nd point

        Returns:
            great circle distance
        """
        if not isintance(aPoint, point):
            return 0 # throw error

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(math.radians, [self.lon, self.lat, aPoint.lon, aPoint.lat])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2.)**2. + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2.)**2.
        c = 2. * math.asin(math.sqrt(a))
        return EARTH_RADIUS * c


class circle(object):
    """
    Doc
    """
    def __init__(self, point, radius):
        self.center = point
        self.radius = radius

    def distance_from_circle_center(self, aCircle):
        """
        return the distance between the center of the 2 circles
        """
        if not isintance(aCircle, circle):
            return 0 # throw error
        return self.center.distance_from_point(aCircle.center)


    def intersection_with_circle(self, aCircle):
        """
        return 2 points as intersection of the 2 circles
        the last return parameters shows if there is a real intersection
            or if it is fake intersection points
        """
        if not isintance(aCircle, circle):
            return 0 # throw error

        does_intersect = self.radius + circle.radius >= self.distance_from_circle_center(aCircle)
        if does_intersect:
            # look for intersections
            """
                p1 = c1.center 
                p2 = c2.center
                r1 = c1.radius
                r2 = c2.radius

                d = get_two_points_distance(p1, p2)
                # if to far away, or self contained - can't be done
                if d >= (r1 + r2) or d <= math.fabs(r1 -r2):
                    return None

                a = (pow(r1, 2) - pow(r2, 2) + pow(d, 2)) / (2*d)
                h  = math.sqrt(pow(r1, 2) - pow(a, 2))
                x0 = p1.x + a*(p2.x - p1.x)/d 
                y0 = p1.y + a*(p2.y - p1.y)/d
                rx = -(p2.y - p1.y) * (h/d)
                ry = -(p2.x - p1.x) * (h / d)
                return [point(x0+rx, y0-ry), point(x0-rx, y0+ry)]
            """
            pass
        else:
            self.is_approximation = True
            # generate fake intersections
            pass


class trilateration:
    """
    Doc
    """

    def __init__(self, circlesList):
        """
        Doc
        """

        # PUBLIC
        self.geolocalized_device = None
        self.is_approximation = False

        # PRIVATE
        self.__circles = circlesList
        self.__level = len(circlesList)
        self.__circles_intersections = []
        
        # compute the trilateration
        self.__compute_intersections()
        self.__compute_geolocalization()


    def __compute_intersections(self):
        """
        generate all the intersections
        """
        if self.__level == 0:
            return 0 # throw error -> we are no magicians
        if self.__level == 1:
            return 0 # throw error -> we are no magicians
        if self.__level == 2:
            return 0 # throw error -> we are no magicians

        self.__circles_intersections = []
        for i, circle in enumerate(self.__circles):
            for j in xrange(i + 1, len(self.__circles))
                inter1, inter2 = circle.intersection_with_circle(self.__circles[j])
                self.__circles_intersections.append(inter1)
                self.__circles_intersections.append(inter2)

    def __compute_geolocalization(self):
        """
        Doc
        """
        mean_lat, mean_lon = .0, .0
        for intersection in self.__circles_intersections:
            mean_lat += intersection.lat
            mean_lon += intersection.lon

        mean_lat /= float(len(self.__circles_intersections))
        mean_lon /= float(len(self.__circles_intersections))

        self.geolocalized_device = point(mean_lat, mean_lon)

