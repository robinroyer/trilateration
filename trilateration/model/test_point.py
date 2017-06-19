from __future__ import absolute_import
import unittest

from ..model.point import Point
# do not forget to use nose2 at root to run test

 
class Test_utils(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST

    def test_point_creation(self):
        p1 = Point(48.84, 2.26)
        self.assertEqual(p1.lat, 48.84)
        self.assertEqual(p1.lon, 2.26)

    # =============================================== ERROR CHECKING

    def test_bad_point_parameter(self):
        self.assertRaises(ValueError, lambda: Point(0,0).distance_from_point(42))

    def test_incorrect_latitude_point(self):
        self.assertRaises(ValueError, lambda: Point(30000 +2j,0))

    def test_incorrect_longitude_point(self):
        self.assertRaises(ValueError, lambda: Point(2,1000000))

if __name__ == '__main__':
    unittest.main()