import unittest

import time
import datetime
from circle import circle
from point import point
# do not forget to use nose2 at root to run test

 
class Test_circle(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST

    def test_circle_creation(self):
        c = circle(point(48.84, 2.26), 300)
        self.assertEqual(c.center.lat, 48.84)
        self.assertEqual(c.center.lon, 2.26)
        self.assertEqual(c.radius, 300)

    # =============================================== ERROR CHECKING

    def test_negative_radius(self):
        self.assertRaises(ValueError, lambda: circle(point(0,0), -1))

    def test_bad_circle_parameter(self):
        self.assertRaises(ValueError, lambda: circle(point(0,0), -1).distance_from_circle_center(42))

if __name__ == '__main__':
    unittest.main()