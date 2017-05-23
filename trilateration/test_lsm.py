import unittest

import time
import datetime

from lsm import lsm
from utils import point, projection, uplink, gateway, SPEED_OF_LIGHT
# do not forget to use nose2 at root to run test

 
class Test_lsm(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    def test_lsm_creation(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)
        g4 = gateway(48.90, 2.40)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = lsm([u1, u2, u3, u4])

        self.assertEqual(solver._level, 4)
        self.assertEqual(solver._uplinks, [u1, u2, u3, u4])

    # =============================================== FUNCTIONNAL TEST
    def test_trilateration_compute_random(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)
        g4 = gateway(48.90, 2.40)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = lsm([u1, u2, u3, u4])

        # user of delta because of 2 occurences of times are different
        self.assertAlmostEqual(solver.geolocalized_device.lat, 48.832071, delta=1.0)
        self.assertAlmostEqual(solver.geolocalized_device.lon, 2.391112, delta=1.0)

    def test_same_time(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)
        g4 = gateway(48.90, 2.40)

        t = int(time.time() * 1000000000)

        u1 = uplink(g1, datetime.datetime.now(), t)
        u2 = uplink(g2, datetime.datetime.now(), t)
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = lsm([ u2, u3, u4])
        self.assertTrue(solver.is_resolved)

    def test_10_uplinks(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)
        g4 = gateway(48.80, 2.22)
        g5 = gateway(48.93, 2.22)
        g6 = gateway(48.73, 2.12)
        g7 = gateway(48.63, 2.02)
        g8 = gateway(48.53, 2.32)
        g9 = gateway(48.87, 2.29)
        g10 = gateway(48.66, 2.24)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))
        u5 = uplink(g5, datetime.datetime.now(), int(time.time() * 1000000000))
        u6 = uplink(g6, datetime.datetime.now(), int(time.time() * 1000000000))
        u7 = uplink(g7, datetime.datetime.now(), int(time.time() * 1000000000))
        u8 = uplink(g8, datetime.datetime.now(), int(time.time() * 1000000000))
        u9 = uplink(g9, datetime.datetime.now(), int(time.time() * 1000000000))
        u10 = uplink(g10, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = lsm([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10])
        self.assertTrue(solver.is_resolved)


    # =============================================== ERROR CHECKING
    def test_only_one_uplink(self):
        g1 = gateway(48.84, 2.26)
        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: lsm([u1]))

    def test_only_two_uplinks(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: lsm([u1, u2]))

    def test_incorrect_param_type(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.8, 2.32)
        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000)) 
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: lsm([u1, u2, .0])) 

    def test_incorrect_projection(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)
        g4 = gateway(48.8, 2.32)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = lsm([u1, u2, u3, u4])
        projection_system = 42
        self.assertRaises(ValueError, lambda: lsm([u1, u2, u3], projection_system)) 

    def test_2_same_gateways(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.84, 2.30)
        g3 = gateway(48.84, 2.30)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: lsm([u1, u2, u2, u2]))


    def test_3_same_uplinks(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: lsm([u1, u2, u2, u2]))

    def test_same_uplink(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.84, 2.30)

        t = int(time.time() * 1000000000)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), t)
        u4 = uplink(g3, datetime.datetime.now(), t)

        self.assertRaises(ValueError, lambda: lsm([u1, u2, u3, u4]))

if __name__ == '__main__':
    unittest.main()