from __future__ import absolute_import

import math
import pyproj
from sympy import Symbol
from sympy.solvers import solve

from ..model.point import Point
from ..model.projection import Projection
from ..utils.tools import is_number

class Circle:
    """Reprensation of a geographic Circle"""
    def __init__(self, a_point, radius):
        """circle constructor
        Args:
            a_point: The center of the Circle (should be a Circle).
            radius: The radius fo the Circle (postif).
        """
        if not isinstance(a_point, Point):
            raise ValueError("Incorrect point")
        if not is_number(radius) or radius < 0:
            raise ValueError("Incorrect Circle radius")
        self.center = a_point
        self.radius = float(radius)

    def __str__(self):
        """Overload __str__ for debug"""
        return "Circle ->\n\tradius: %f\n\tcenter => latitude: %f, longitude: %f" % (self.center.lat, self.center.lon, self.radius)


    def does_intersect(self, a_circle):
        """Check if 2 Circles have intersections.

        Args:
            a_circle: The other Circle we shoud compare to self.

        Returns:
            True if there is interections. False otherwise
        """
        return self.radius + a_circle.radius >= self.center.distance_from_point(a_circle.center)


    def does_contain(self, a_circle):
        """Check one of the 2 Circles contains the other one

        Args:
            a_circle: The other Circle we shoud compare to self.

        Returns:
            True if the self or a_circle contains the other Circle

        """
        return not self.does_intersect(a_circle) and \
        max(self.radius, a_circle.radius) < self.center.distance_from_point(a_circle.center)


    def distance_from_circle_center(self, a_circle):
        """Compute the distance between the center of self and the center the Circle parameter

        Args:
            a_circle: The first parameter.

        Returns:
            The distance between the 2 Circles
        """
        if not isinstance(a_circle, Circle):
            raise ValueError("Parameter is not a Circle")
        return self.center.distance_from_point(a_circle.center)


    def intersection_with_circle(self, a_circle, proj=Projection()):
        """Return Two intersection Points if they exist and generate 2 false intersection Points otherwise

        Args:
            a_circle: The second Circle to consider.
            proj: The Projection system to go from Lat/long tuple to x/y coordinate.

        Returns:
            The 2 Points(intersection or generated), boolean indicating if the intersections are generated

        """
        if not isinstance(a_circle, Circle):
            raise ValueError("parameter is not a Circle")

        # Check if we approximate intersection or not
        approximation = not self.does_intersect(a_circle) or self.does_contain(a_circle)

        #  ============================================================= COMPUTE 
        # Projection over x, y
        self_x, self_y = proj.lat_long_to_x_y(self.center.lat, self.center.lon)
        a_circle_x, a_circle_y = proj.lat_long_to_x_y(a_circle.center.lat, a_circle.center.lon)
        # symbole for equation
        x, y = Symbol('x'), Symbol('y')

        equations = []
        equations.append((self_x - x)**2 + (self_y - y)**2  - self.radius**2 )
        equations.append((a_circle_x - x)**2 + (a_circle_y - y)**2  - a_circle.radius**2 )

        res = solve( equations, x, y)

        if not isinstance(res[0], tuple): # no result Point
            return None, None, approximation
        elif len(res) == 2:
            lo1, la1 = proj.x_y_to_long_lat(complex(res[0][0]).real, complex(res[0][1]).real)
            lo2, la2 = proj.x_y_to_long_lat(complex(res[1][0]).real, complex(res[1][1]).real)
            return Point(la1, lo1), Point(la2, lo2), approximation
        else:
            lo1, la1 = proj.x_y_to_long_lat(complex(res[0][0]).real, complex(res[0][1]).real)
            return Point(la1, lo1), Point(la2, lo2), approximation
