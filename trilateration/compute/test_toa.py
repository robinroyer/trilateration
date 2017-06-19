from __future__ import absolute_import

import unittest

import time
import datetime

from ..compute.toa import Toa
from ..model.uplink import Uplink
from ..model.gateway import Gateway
from ..utils.tools import SPEED_OF_LIGHT
from ..model.projection import Projection
 
class Test_toa(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    def test_trilateration_creation(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = Toa([u1, u2, u3])

        self.assertEqual(solver._level, 3)
        self.assertEqual(solver._uplinks, [u1, u2, u3])

    # =============================================== FUNCTIONNAL TEST
    def test_trilateration_compute_random(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = Toa([u1, u2, u3])
        # user of delta because of 2 occurences of times are different
        self.assertAlmostEqual(solver.geolocalized_device.lat, 48.808139705595316, delta=1.0)
        self.assertAlmostEqual(solver.geolocalized_device.lon, 2.308668, delta=1.0)

    def test_trilateration_compute_random(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)

        u1 = Uplink(g1, datetime.datetime.now(), 1495456868630584064)
        u2 = Uplink(g2, datetime.datetime.now(), 1495456868630585856)
        u3 = Uplink(g3, datetime.datetime.now(), 1495456868630585856)

        solver = Toa([u1, u2, u3])
        # user of delta because of 2 occurences of times are different
        self.assertAlmostEqual(solver.geolocalized_device.lat, 48.819999, delta=.000001)
        self.assertAlmostEqual(solver.geolocalized_device.lon, 2.286716, delta=.000001)

    def test_same_time(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)

        t = int(time.time() * 1000000000)

        u1 = Uplink(g1, datetime.datetime.now(), t)
        u2 = Uplink(g2, datetime.datetime.now(), t)
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = Toa([u1, u2, u3])
        self.assertFalse(solver.is_resolved)

    def test_same_Gateway(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.84, 2.30)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = Toa([u1, u2, u3])
        self.assertFalse(solver.is_resolved)

    def test_same_uplink(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.84, 2.30)

        t = int(time.time() * 1000000000)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), t)
        u3 = Uplink(g3, datetime.datetime.now(), t)

        solver = Toa([u1, u2, u3])
        self.assertFalse(solver.is_resolved)

    # =============================================== ERROR CHECKING
    def test_only_one_uplink(self):
        g1 = Gateway(48.84, 2.26)
        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Toa([u1]))

    def test_only_two_uplinks(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Toa([u1, u2]))

    def test_four_gateways(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)
        g4 = Gateway(48.80, 2.22)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = Uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Toa([u1, u2, u3, u4]))

    def test_incorrect_param_type(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000)) 
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Toa([u1, u2, .0])) 

    def test_incorrect_projection(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = Toa([u1, u2, u3])
        projection_system = 42
        self.assertRaises(ValueError, lambda: Toa([u1, u2, u3], projection_system)) 

if __name__ == '__main__':
    unittest.main()