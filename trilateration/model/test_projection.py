import unittest

import time
import datetime
from projection import projection
# do not forget to use nose2 at root to run test

 
class Test_projection(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    
    def test_circle_creation(self):
        c = circle(point(48.84, 2.26), 300)
        self.assertEqual(c.center.lat, 48.84)
        self.assertEqual(c.center.lon, 2.26)
        self.assertEqual(c.radius, 300)

    # =============================================== ERROR CHECKING

    def test_incorrect_projection_parameter(self):
        self.assertRaises(ValueError, lambda: None)

if __name__ == '__main__':
    unittest.main()