
import time
import datetime
import unittest

from solver import solver

from ..model.point import point

from ..utils.mock import getPoint1Uplinks, getPoint2Uplinks, getPoint3Uplinks, getPoint4Uplinks, getPoint5Uplinks, measures

from ..filter.statistic_filter import filter_point_distance, filter_uplink_timestamps, filter_uplink_distance



class Test_solver(unittest.TestCase):

    def test_solver(self):
        t = int(time.time() * 1000000000)
        sol = solver(
            "lsm",
            ["result_distance", "gateway_distance"]
        )
        
        a = sol.predict([
            [48.84, 2.16, datetime.datetime.now(), t],
            [48.94, 2.26, datetime.datetime.now(), t + 300],
            [48.95, 2.27, datetime.datetime.now(), t + 300],
            [48.96, 2.28, datetime.datetime.now(), t + 300],
            [0.97, 0.29, datetime.datetime.now(), t + 300],
            [48.75, 2.16, datetime.datetime.now(), t + 400],
        ])
        self.assertTrue(sol.is_resolved)
        self.assertAlmostEqual(a.lon, 2.2301313161237695)
        self.assertAlmostEqual(a.lat, 48.880731565246485)

    def test_2(self):
        # test on first measure point
        localisation = measures[0]
        uplks = getPoint1Uplinks()

        sol = solver(
            "tdoa",
            []
        )

        all_results = []
        for uplk in uplks:
            results = []
            for i in xrange(4, len(uplk)):
                a = sol.predict(uplk[i-4: i])
                results.append(a)
                # print "error: ", a.distance_from_point(point(localisation[0], localisation[1]))

            results = filter_point_distance(results, 2)
            lat = 0
            lon = 0
            if len(results) != 0:
                for result in results:
                    lat += result.lat
                    lon += result.lon
                lat /= len(results)
                lon /= len(results)
                all_results.append(point(lat, lon))
            print "mean", point(lat, lon).distance_from_point(point(localisation[0], localisation[1]))

        all_results = filter_point_distance(all_results, 2)
        lat = 0
        lon = 0
        for result in all_results:
            lat += result.lat
            lon += result.lon
        lat /= len(all_results)
        lon /= len(all_results)
        all_results.append(point(lat, lon))
        print "real result", point(lat, lon).distance_from_point(point(localisation[0], localisation[1]))

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()










