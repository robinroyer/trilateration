from __future__ import absolute_import
import unittest

import time
import datetime

from ..model.projection import Projection
# do not forget to use nose2 at root to run test

 
class Test_Projection(unittest.TestCase):
    
    # =============================================== OBJECT UNIT TEST
    def test_correct_projection(self):

        proj = Projection()
        x, y = proj.lat_long_to_x_y(48.84, 2.26)
        self.assertAlmostEqual(594327.720979058, x)
        self.assertAlmostEqual(2426852.1010616063, y)
        lon, lat = proj.x_y_to_long_lat(x, y)
        self.assertAlmostEqual(48.83999999998599, lat)
        self.assertAlmostEqual(2.2600000000000007, lon)

    # =============================================== ERROR CHECKING

    def test_incorrect_projection_parameter(self):
        self.assertRaises(ValueError, lambda: Projection(42))

if __name__ == '__main__':
    unittest.main()