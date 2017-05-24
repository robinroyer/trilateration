
import math
import pyproj
from sympy import Symbol
from sympy.solvers import solve

from point import point
from utils.utils import is_number
from projection import projection

class circle:
    """Reprensation of a geographic circle"""
    def __init__(self, a_point, radius):
        """circle constructor
        Args:
            a_point: The center of the circle (should be a circle).
            radius: The radius fo the circle (postif).
        """
        if not isinstance(a_point, point):
            raise ValueError("Incorrect point")
        if not is_number(radius) or radius < 0:
            raise ValueError("Incorrect circle radius")
        self.center = a_point
        self.radius = float(radius)

    def __str__(self):
        """Overload __str__ for debug"""
        return "Circle ->\n\tradius: %f\n\tcenter => latitude: %f, longitude: %f" % (self.center.lat, self.center.lon, self.radius)


    def does_intersect(self, a_circle):
        """Check if 2 circles have intersections.

        Args:
            a_circle: The other circle we shoud compare to self.

        Returns:
            True if there is interections. False otherwise
        """
        return self.radius + a_circle.radius >= self.center.distance_from_point(a_circle.center)


    def does_contain(self, a_circle):
        """Check one of the 2 circles contains the other one

        Args:
            a_circle: The other circle we shoud compare to self.

        Returns:
            True if the self or a_circle contains the other circle

        """
        return not self.does_intersect(a_circle) and \
        max(self.radius, a_circle.radius) < self.center.distance_from_point(a_circle.center)


    def distance_from_circle_center(self, a_circle):
        """Compute the distance between the center of self and the center the circle parameter

        Args:
            a_circle: The first parameter.

        Returns:
            The distance between the 2 circles
        """
        if not isinstance(a_circle, circle):
            raise ValueError("Parameter is not a circle")
        return self.center.distance_from_point(a_circle.center)


    def intersection_with_circle(self, a_circle, proj=projection()):
        """Return Two intersection points if they exist and generate 2 false intersection points otherwise

        Args:
            a_circle: The second circle to consider.
            proj: The projection system to go from Lat/long tuple to x/y coordinate.

        Returns:
            The 2 points(intersection or generated), boolean indicating if the intersections are generated

        """
        if not isinstance(a_circle, circle):
            raise ValueError("parameter is not a circle")

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
