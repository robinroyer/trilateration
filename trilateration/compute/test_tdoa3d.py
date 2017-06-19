from __future__ import absolute_import

import unittest

import time
import datetime

from ..compute.tdoa3d import Tdoa3d
from ..model.uplink import Uplink
from ..model.gateway import Gateway
from ..utils.tools import SPEED_OF_LIGHT
from ..model.projection import Projection
# do not forget to use nose2 at root to run test

 
class Test_tdoa(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    def test_tdoa_creation(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)
        g4 = Gateway(48.90, 2.40)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = Uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = Tdoa3d([u1, u2, u3, u4])

        self.assertEqual(solver._level, 4)
        self.assertEqual(solver._uplinks, [u1, u2, u3, u4])

    # =============================================== FUNCTIONNAL TEST
    def test_trilateration_compute_random(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)
        g4 = Gateway(48.90, 2.40)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = Uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = Tdoa3d([u1, u2, u3, u4])

        # user of delta because of 2 occurences of times are different
        self.assertAlmostEqual(solver.geolocalized_device.lat, 48.832071, delta=1.0)
        self.assertAlmostEqual(solver.geolocalized_device.lon, 2.391112, delta=1.0)

    def test_same_time(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)
        g4 = Gateway(48.90, 2.40)

        t = int(time.time() * 1000000000)

        u1 = Uplink(g1, datetime.datetime.now(), t)
        u2 = Uplink(g2, datetime.datetime.now(), t)
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = Uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = Tdoa3d([u1, u2, u3, u4])
        self.assertTrue(solver.is_resolved)

    def test_2_same_gateways(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.84, 2.30)
        g3 = Gateway(48.84, 2.30)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Tdoa3d([u1, u2, u2, u2]))


    def test_3_same_uplinks(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Tdoa3d([u1, u2, u2, u2]))

    def test_same_uplink(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.84, 2.30)

        t = int(time.time() * 1000000000)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), t)
        u4 = Uplink(g3, datetime.datetime.now(), t)

        self.assertRaises(ValueError, lambda: Tdoa3d([u1, u2, u3, u4]))

    # =============================================== ERROR CHECKING
    def test_only_one_uplink(self):
        g1 = Gateway(48.84, 2.26)
        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Tdoa3d([u1]))

    def test_only_two_uplinks(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Tdoa3d([u1, u2]))

    def test_five_gateways(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)
        g4 = Gateway(48.80, 2.22)
        g5 = Gateway(48.83, 2.2)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = Uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))
        u5 = Uplink(g5, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Tdoa3d([u1, u2, u3, u4, u5]))

    def test_incorrect_param_type(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.8, 2.32)
        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000)) 
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))

        self.assertRaises(ValueError, lambda: Tdoa3d([u1, u2, .0])) 

    def test_incorrect_projection(self):
        g1 = Gateway(48.84, 2.26)
        g2 = Gateway(48.84, 2.30)
        g3 = Gateway(48.80, 2.30)
        g4 = Gateway(48.8, 2.32)

        u1 = Uplink(g1, datetime.datetime.now(), int(time.time() * 1000000000))
        u2 = Uplink(g2, datetime.datetime.now(), int(time.time() * 1000000000))
        u3 = Uplink(g3, datetime.datetime.now(), int(time.time() * 1000000000))
        u4 = Uplink(g4, datetime.datetime.now(), int(time.time() * 1000000000))

        solver = Tdoa3d([u1, u2, u3, u4])
        Projection_system = 42
        self.assertRaises(ValueError, lambda: Tdoa3d([u1, u2, u3], Projection_system)) 

if __name__ == '__main__':
    unittest.main()