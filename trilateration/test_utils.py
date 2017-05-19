import unittest

from utils import circle, point, projection
# do not forget to use nose2 at root to run test

 
class Test_trilateration(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    def test_circle_creation(self):
        c = circle(point(48.84, 2.26), 300)
        self.assertEqual(c.center.lat, 48.84)
        self.assertEqual(c.center.lon, 2.26)
        self.assertEqual(c.radius, 300)

    def test_point_creation(self):
        p1 = point(48.84, 2.26)
        self.assertEqual(p1.lat, 48.84)
        self.assertEqual(p1.lon, 2.26)

    # =============================================== ERROR CHECKING
    def test_negative_radius(self):
        self.assertRaises(ValueError, lambda: circle(point(0,0), -1))

    def test_bad_circle_parameter(self):
        self.assertRaises(ValueError, lambda: circle(point(0,0), -1).distance_from_circle_center(42))

    def test_bad_point_parameter(self):
        self.assertRaises(ValueError, lambda: point(0,0).distance_from_point(42))

    def test_incorrect_latitude(self):
        self.assertRaises(ValueError, lambda: point(30000 +2j,0))

    def test_incorrect_longitude(self):
        self.assertRaises(ValueError, lambda: point(2,1000000))

if __name__ == '__main__':
    unittest.main()