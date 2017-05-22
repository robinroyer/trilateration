import unittest

import time
import datetime
from toa import toa
from utils import circle, point, projection, uplink, gateway, SPEED_OF_LIGHT
# do not forget to use nose2 at root to run test

 
class Test_toa(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    def test_trilateration_creation(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = toa([u1, u2, u3])

        self.assertEqual(solver._level, 3)
        self.assertEqual(solver._uplinks, [u1, u2, u3])

    # =============================================== FUNCTIONNAL TEST
    def test_complete_approximation(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = toa([u1, u2, u3])
        self.assertAlmostEqual(solver.geolocalized_device.lat, 48.808139705595316, delta=1.0)
        self.assertAlmostEqual(solver.geolocalized_device.lon, 2.308668, delta=1.0)

    # def test_same_circle(self):
    #     c1 = circle(point(48.84, 2.26), 3000)
    #     c2 = circle(point(48.84, 2.26), 3000)
    #     c3 = circle(point(48.80, 2.30), 3500)

    #     trilat = trilateration([c1, c2, c3])
    #     self.assertAlmostEqual(trilat.geolocalized_device.lat, 48.822284944905945)
    #     self.assertAlmostEqual(trilat.geolocalized_device.lon, 2.27772629824793)

    # def test_area_intersection(self):
    #     c1 = circle(point(48.84, 2.26), 3000)
    #     c2 = circle(point(48.84, 2.30), 5000)
    #     c3 = circle(point(48.80, 2.30), 3500)

    #     trilat = trilateration([c1, c2, c3])

    #     self.assertFalse(trilat.is_approximation)
    #     self.assertAlmostEqual(trilat.geolocalized_device.lat, 48.82313276075889)
    #     self.assertAlmostEqual(trilat.geolocalized_device.lon, 2.273550537885488)

    # def test_two_circles_intersection(self):
    #     c1 = circle(point(48.84, 2.26), 3000)
    #     c2 = circle(point(48.84, 2.30), 5000)
    #     c3 = circle(point(48.80, 2.30), 3)

    #     trilat = trilateration([c1, c2, c3])

    #     self.assertTrue(trilat.is_approximation)

    # # =============================================== ERROR CHECKING
    # def test_only_one_circle(self):
    #     c1 = circle(point(48.84, 2.30), 5000)
    #     self.assertRaises(ValueError, lambda: trilateration([c1]))

    # def test_only_two_circles(self):
    #     c1 = circle(point(48.84, 2.30), 5000)
    #     c2 = circle(point(48.80, 2.30), 3500)
    #     self.assertRaises(ValueError, lambda: trilateration([c1, c2]))

    # def test_four_circles(self):
    #     c1 = circle(point(48.84, 2.30), 5000)
    #     c2 = circle(point(48.80, 2.30), 3500)
    #     c3 = circle(point(48.80, 2.30), 3500)
    #     c4 = circle(point(48.80, 2.30), 3500)
    #     self.assertRaises(ValueError, lambda: trilateration([c1, c2, c3, c4]))

    # def test_incorrect_param_type(self):
    #     c1 = circle(point(48.84, 2.30), 5000)
    #     c2 = circle(point(48.80, 2.30), 3500)
    #     self.assertRaises(ValueError, lambda: trilateration([c1, c2, .0])) 

    # def test_incorrect_projection(self):
    #     c1 = circle(point(48.84, 2.30), 5000)
    #     c2 = circle(point(48.80, 2.30), 3500)
    #     c3 = circle(point(48.80, 2.30), 3500)
    #     projection_system = 42
    #     self.assertRaises(ValueError, lambda: trilateration([c1, c2, c3], projection_system)) 

if __name__ == '__main__':
    unittest.main()