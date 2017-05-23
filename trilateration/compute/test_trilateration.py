import unittest

from trilateration import trilateration
from trilateration.model.point import point
from trilateration.model.uplink import uplink
from trilateration.model.circle import circle
from trilateration.model.gateway import gateway
from trilateration.utils.utils import SPEED_OF_LIGHT
from trilateration.model.projection import projection
# do not forget to use nose2 at root to run test

 
class Test_trilateration(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    def test_trilateration_creation(self):
        c1 = circle(point(48.84, 2.26), 300)
        c2 = circle(point(48.84, 2.30), 5)
        c3 = circle(point(48.80, 2.30), 350)

        trilat = trilateration([c1, c2, c3])

        self.assertEqual(trilat._level, 3)
        self.assertEqual(trilat._circles, [c1, c2, c3])

    # =============================================== FUNCTIONNAL TEST
    def test_complete_approximation(self):
        c1 = circle(point(48.84, 2.26), 300)
        c2 = circle(point(48.84, 2.30), 5)
        c3 = circle(point(48.80, 2.30), 350)

        trilat = trilateration([c1, c2, c3])
        self.assertTrue(trilat.is_approximation)
        self.assertAlmostEqual(trilat.geolocalized_device.lat, 48.8267167301514)
        self.assertAlmostEqual(trilat.geolocalized_device.lon, 2.28673111454713)

    def test_same_circle(self):
        c1 = circle(point(48.84, 2.26), 3000)
        c2 = circle(point(48.84, 2.26), 3000)
        c3 = circle(point(48.80, 2.30), 3500)

        trilat = trilateration([c1, c2, c3])
        self.assertAlmostEqual(trilat.geolocalized_device.lat, 48.822284944905945)
        self.assertAlmostEqual(trilat.geolocalized_device.lon, 2.27772629824793)

    def test_area_intersection(self):
        c1 = circle(point(48.84, 2.26), 3000)
        c2 = circle(point(48.84, 2.30), 5000)
        c3 = circle(point(48.80, 2.30), 3500)

        trilat = trilateration([c1, c2, c3])

        self.assertFalse(trilat.is_approximation)
        self.assertAlmostEqual(trilat.geolocalized_device.lat, 48.82313276075889)
        self.assertAlmostEqual(trilat.geolocalized_device.lon, 2.273550537885488)

    def test_two_circles_intersection(self):
        c1 = circle(point(48.84, 2.26), 3000)
        c2 = circle(point(48.84, 2.30), 5000)
        c3 = circle(point(48.80, 2.30), 3)

        trilat = trilateration([c1, c2, c3])

        self.assertTrue(trilat.is_approximation)

    # =============================================== ERROR CHECKING
    def test_only_one_circle(self):
        c1 = circle(point(48.84, 2.30), 5000)
        self.assertRaises(ValueError, lambda: trilateration([c1]))

    def test_only_two_circles(self):
        c1 = circle(point(48.84, 2.30), 5000)
        c2 = circle(point(48.80, 2.30), 3500)
        self.assertRaises(ValueError, lambda: trilateration([c1, c2]))

    def test_four_circles(self):
        c1 = circle(point(48.84, 2.30), 5000)
        c2 = circle(point(48.80, 2.30), 3500)
        c3 = circle(point(48.80, 2.30), 3500)
        c4 = circle(point(48.80, 2.30), 3500)
        self.assertRaises(ValueError, lambda: trilateration([c1, c2, c3, c4]))

    def test_incorrect_param_type(self):
        c1 = circle(point(48.84, 2.30), 5000)
        c2 = circle(point(48.80, 2.30), 3500)
        self.assertRaises(ValueError, lambda: trilateration([c1, c2, .0])) 

    def test_incorrect_projection(self):
        c1 = circle(point(48.84, 2.30), 5000)
        c2 = circle(point(48.80, 2.30), 3500)
        c3 = circle(point(48.80, 2.30), 3500)
        projection_system = 42
        self.assertRaises(ValueError, lambda: trilateration([c1, c2, c3], projection_system)) 

if __name__ == '__main__':
    unittest.main()