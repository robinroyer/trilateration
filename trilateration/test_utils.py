import unittest

import time
import datetime
from utils import circle, point, projection, gateway, uplink
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

    def test_gateway_creation(self):
        g = gateway(48.84, 2.26)
        self.assertEqual(g.lat, 48.84)
        self.assertEqual(g.lon, 2.26)

    def test_uplink_creation(self):
        g = gateway(48.84, 2.26)
        t = int(time.time() * 1000000000)   
        d = datetime.datetime.now()
        u = uplink(g, d, t)

        self.assertEqual(u.gateway.lat, 48.84)
        self.assertEqual(u.gateway.lon, 2.26)
        self.assertEqual(u.timestamp, t)
        self.assertEqual(u.arrival_date, d)

    # =============================================== ERROR CHECKING
    def test_negative_radius(self):
        self.assertRaises(ValueError, lambda: circle(point(0,0), -1))

    def test_bad_circle_parameter(self):
        self.assertRaises(ValueError, lambda: circle(point(0,0), -1).distance_from_circle_center(42))

    def test_bad_point_parameter(self):
        self.assertRaises(ValueError, lambda: point(0,0).distance_from_point(42))

    def test_incorrect_latitude_point(self):
        self.assertRaises(ValueError, lambda: point(30000 +2j,0))

    def test_incorrect_longitude_point(self):
        self.assertRaises(ValueError, lambda: point(2,1000000))

    def test_incorrect_latitude_gateway(self):
        self.assertRaises(ValueError, lambda: gateway(30000 +2j,0))

    def test_incorrect_longitude_gateway(self):
        self.assertRaises(ValueError, lambda: gateway(2,1000000))

    def test_incorrect_timestamp_uplink(self):
        g = gateway(48.84, 2.26)
        self.assertRaises(ValueError, lambda: uplink(g, datetime.datetime.now(), "coucou"))

    def test_incorrect_gateway_uplink(self):
        self.assertRaises(ValueError, lambda: uplink("coucou", datetime.datetime.now(), int(time.time() * 1000000000)))

if __name__ == '__main__':
    unittest.main()