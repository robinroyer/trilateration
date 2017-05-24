import unittest

import time
import datetime
from projection import projection
from circle import circle
from point import point
# do not forget to use nose2 at root to run test

 
class Test_projection(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    def test_correct_projection(self):

        proj = projection()
        x, y = proj.lat_long_to_x_y(48.84, 2.26)
        self.assertEqual(594327.720979058, x)
        self.assertEqual(2426852.1010616063, y)
        lon, lat = proj.x_y_to_long_lat(x, y)
        self.assertEqual(48.83999999998599, lat)
        self.assertEqual(2.2600000000000007, lon)

    # =============================================== ERROR CHECKING

    def test_incorrect_projection_parameter(self):
        self.assertRaises(ValueError, lambda: projection(42))

if __name__ == '__main__':
    unittest.main()