import time
import unittest
import datetime
import numpy as np

from trilateration.model.point import point
from trilateration.model.uplink import uplink
from trilateration.model.gateway import gateway
from statistic_filter import filter_uplink_timestamps, filter_point_distance



class Test_filtering_functions(unittest.TestCase):

    def test_filter_uplink_timestamps(self):
        uplinks = []
        for i in xrange(0,10):
            g = gateway(48.84, 2.26)
            d = datetime.datetime.now()
            t = int(time.time() * 1000000000)  
            uplinks.append(uplink(g, d, t))

        uplinks[2].timestamp = int(time.time() * 1000000000)  + 4000000
        res =  filter_uplink_timestamps(uplinks, 2.5)
        self.assertEqual(len(uplinks), 10)
        self.assertEqual(len(res), 9)

    def test_filter_point_distance(self):
        points = []
        for i in xrange(0,10):
            points.append(point(48.84 + i, 2.26 + i))
        res =  filter_point_distance(points, 1)
        self.assertEqual(len(points), 10)
        self.assertEqual(len(res), 6)


if __name__ == '__main__':
    unittest.main()
