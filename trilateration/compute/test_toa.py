import unittest

import time
import datetime

from toa import toa
from model.point import point
from model.uplink import uplink
from model.gateway import gateway
from utils.utils import SPEED_OF_LIGHT
from model.projection import projection
 
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
    def test_trilateration_compute_random(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = toa([u1, u2, u3])
        # user of delta because of 2 occurences of times are different
        self.assertAlmostEqual(solver.geolocalized_device.lat, 48.808139705595316, delta=1.0)
        self.assertAlmostEqual(solver.geolocalized_device.lon, 2.308668, delta=1.0)

    def test_trilateration_compute_random(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)

        u1 = uplink(g1, datetime.datetime.now(), 1495456868630584064)
        u2 = uplink(g2, datetime.datetime.now(), 1495456868630585856)
        u3 = uplink(g3, datetime.datetime.now(), 1495456868630585856)

        solver = toa([u1, u2, u3])
        # user of delta because of 2 occurences of times are different
        self.assertAlmostEqual(solver.geolocalized_device.lat, 48.819999, delta=.000001)
        self.assertAlmostEqual(solver.geolocalized_device.lon, 2.286716, delta=.000001)

    def test_same_time(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)

        t = int(time.time() * 1000000000)

        u1 = uplink(g1, datetime.datetime.now(), t)
        u2 = uplink(g2, datetime.datetime.now(), t)
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = toa([u1, u2, u3])
        self.assertFalse(solver.is_resolved)

    def test_same_gateway(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.84, 2.30)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = toa([u1, u2, u3])
        self.assertFalse(solver.is_resolved)

    def test_same_uplink(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.84, 2.30)

        t = int(time.time() * 1000000000)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), t)
        u3 = uplink(g3, datetime.datetime.now(), t)

        solver = toa([u1, u2, u3])
        self.assertFalse(solver.is_resolved)

    # =============================================== ERROR CHECKING
    def test_only_one_uplink(self):
        g1 = gateway(48.84, 2.26)
        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: toa([u1]))

    def test_only_two_uplinks(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: toa([u1, u2]))

    def test_four_gateways(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)
        g4 = gateway(48.80, 2.22)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: toa([u1, u2, u3, u4]))

    def test_incorrect_param_type(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000)) 
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: toa([u1, u2, .0])) 

    def test_incorrect_projection(self):
        g1 = gateway(48.84, 2.26)
        g2 = gateway(48.84, 2.30)
        g3 = gateway(48.80, 2.30)

        u1 = uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = toa([u1, u2, u3])
        projection_system = 42
        self.assertRaises(ValueError, lambda: toa([u1, u2, u3], projection_system)) 

if __name__ == '__main__':
    unittest.main()