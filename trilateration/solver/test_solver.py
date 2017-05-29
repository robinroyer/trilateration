
import time
import datetime
import unittest

from solver import solver


class Test_solver(unittest.TestCase):

    def test_solver(self):
        t = int(time.time() * 1000000000)
        sol = solver(
            "lsm",
            ["timestamp"]
        )
        
        a = sol.predict([
            [48.84, 2.16, datetime.datetime.now(), t],
            [48.94, 2.26, datetime.datetime.now(), t + 300],
            [48.95, 2.27, datetime.datetime.now(), t + 300],
            [48.96, 2.28, datetime.datetime.now(), t + 300],
            [48.97, 2.29, datetime.datetime.now(), t + 300],
            [48.75, 2.16, datetime.datetime.now(), t + 20000],
        ])
        self.assertTrue(sol.is_resolved)
        self.assertAlmostEqual(a.lon, 2.2301313161237695)
        self.assertAlmostEqual(a.lat, 48.880731565246485)


if __name__ == '__main__':
    unittest.main()










