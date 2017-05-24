import unittest

from gateway import gateway
# do not forget to use nose2 at root to run test


class Test_gateway(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST

    def test_gateway_creation(self):
        g = gateway(48.84, 2.26)
        self.assertEqual(g.lat, 48.84)
        self.assertEqual(g.lon, 2.26)

    # =============================================== ERROR CHECKING

    def test_incorrect_latitude_gateway(self):
        self.assertRaises(ValueError, lambda: gateway(30000 +2j,0))

    def test_incorrect_longitude_gateway(self):
        self.assertRaises(ValueError, lambda: gateway(2,1000000))

if __name__ == '__main__':
    unittest.main()