import unittest

import time
import datetime
from uplink import uplink
from uplink import uplink
from gateway import gateway
# do not forget to use nose2 at root to run test

 
class Test_uplink(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST

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

    def test_incorrect_timestamp_uplink(self):
        g = gateway(48.84, 2.26)
        self.assertRaises(ValueError, lambda: uplink(g, datetime.datetime.now(), "coucou"))

    def test_incorrect_gateway_uplink(self):
        self.assertRaises(ValueError, lambda: uplink("coucou", datetime.datetime.now(), int(time.time() * 1000000000)))

if __name__ == '__main__':
    unittest.main()