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

    def test_filter_uplink_timestamps_negative_one_uplink(self):
        uplinks = []
        g = gateway(48.84, 2.26)
        d = datetime.datetime.now()
        t = int(time.time() * 1000000000)  
        uplinks.append(uplink(g, d, t))

        res =  filter_uplink_timestamps(uplinks, 0)
        self.assertEqual(len(uplinks), 1)
        self.assertEqual(len(res), 1)

    def test_filter_point_distance_negative_one_point(self):
        points = []
        points.append(point(48.84, 2.26))
        res =  filter_point_distance(points, 0)
        self.assertEqual(len(points), 1)
        self.assertEqual(len(res), 1)

    def test_filter_uplink_timestamps_negative_param(self):
        uplinks = []
        g = gateway(48.84, 2.26)
        d = datetime.datetime.now()
        t = int(time.time() * 1000000000)  
        uplinks.append(uplink(g, d, t))
        uplinks.append(uplink(g, d, t))

        res =  filter_uplink_timestamps(uplinks, -2.5)
        self.assertEqual(len(uplinks), 2)
        self.assertEqual(len(res), 2)

    def test_filter_point_distance_negative_param(self):
        points = []
        points.append(point(48.84, 2.26))
        points.append(point(48.84, 2.26))
        res =  filter_point_distance(points, -1)
        self.assertEqual(len(points), 2)
        self.assertEqual(len(res), 2)

    def test_filter_empty_uplink_distance(self):
        points = []
        res =  filter_point_distance(points, -1)
        self.assertEqual(len(points), 0)
        self.assertEqual(len(res), 0)

    def test_filter_empty_point_distance(self):
        points = []
        res =  filter_point_distance(points, 1)
        self.assertEqual(len(points), 0)
        self.assertEqual(len(res), 0)




if __name__ == '__main__':
    unittest.main()
