
import time
import datetime

from ..compute.lsm import lsm
from ..compute.tdoa import tdoa
from ..compute.toa import toa

from ..filter.statistic_filter import filter_point_distance, filter_uplink_timestamps

from ..model.gateway import gateway
from ..model.uplink import uplink

class solver:
    """Solver is the high level class of this lib

        Args:
            compute: string ["auto", "lsm", "tdoa", "toa"]
            filter: array ["timestamp", "distance"]
            TODO: callable as filter ?
            filter_params {} key: timestamp, distance
            data [] : array of array [lat, long , date, ts]
    """

    LSM = "lsm"
    TOA = "toa"
    TDOA = "tdoa"
    DISTANCE = "distance"
    TIMESTAMP = "timestamp"


    # TODO add kalman
    def __init__(self, compute="auto", filter=["timestamp", "distance"], filter_params = {}):
        self.is_resolved = False
        self.compute = compute
        self.filter = filter
        self.filter_params = filter_params


    def predict(self, data = []):

        # generate uplink list from data
        uplinks = []
        for item in data:
            uplinks.append(uplink(gateway(item[0], item[1]), item[2], item[3]))

        # Upstream filtering
        if self.TIMESTAMP in self.filter:
            if self.TIMESTAMP in self.filter_params.keys():
                uplinks = filter_uplink_timestamps(uplinks, self.filter_params[self.TIMESTAMP])
            else:
                uplinks = filter_uplink_timestamps(uplinks)

        # Choose compute algorithm
        if self.compute == self.TDOA:
            self.algorithm = tdoa(uplinks)
        elif self.compute == self.TOA:
            self.algorithm = toa(uplinks)
        elif self.compute == self.LSM:
            self.algorithm = lsm(uplinks)
        else:
            self._choose_auto_compute(uplinks)

        # Downstream filtering
        if self.DISTANCE in self.filter and self.compute == self.LSM and len(self.algorithm._intersections) > 1:
            if self.DISTANCE in self.filter_params.keys():
                solutions = filter_point_distance(self.algorithm._intersections, self.filter_params[self.DISTANCE])
            else:
                solutions = filter_point_distance(self.algorithm._intersections)

            mean_lat, mean_lon = .0, .0
            for intersection in self.algorithm._intersections:
                mean_lat += intersection.lat
                mean_lon += intersection.lon

            mean_lat /= float(len(self.algorithm._intersections))
            mean_lon /= float(len(self.algorithm._intersections))

            self.is_resolved = True
            return point(mean_lat, mean_lon)
        elif self.algorithm.is_resolved:
            self.is_resolved = True
            return self.algorithm.geolocalized_device
        return None


    def _choose_auto_compute(self, params = []):
        if len(params) < 3 :
            raise ValueError("too few value for solving. TODO: approximation ? kalman filter")
        elif len(params) == 3:
            self.algorithm = toa(params)
        elif len(params) == 4:
            self.algorithm = tdoa(params)
        else:
            self.algorithm = lsm(params)

if __name__ == '__main__':
    solver = solver(
        "tdoa",
        ["timestamp"],
        [
            [48.84, 2.26, datetime.datetime.now(), int(time.time() * 1000000000)],
            [48.94, 2.26, datetime.datetime.now(), int(time.time() * 1000000000)],
            [48.74, 2.16, datetime.datetime.now(), int(time.time() * 1000000000)],
            [48.54, 2.06, datetime.datetime.now(), int(time.time() * 1000000000)]
        ]
    )












