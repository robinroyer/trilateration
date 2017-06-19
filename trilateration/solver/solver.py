from __future__ import absolute_import

import time
import datetime
import numpy as np
import matplotlib.pyplot as plt

from ..compute.lsm import Lsm
from ..compute.tdoa import Tdoa
from ..compute.tdoa3d import Tdoa3d
from ..compute.toa import Toa

from ..filtering.statistic_filter import filter_point_distance, filter_uplink_timestamps, filter_uplink_distance
from ..filtering.adaptive_filtering import AKF_Filter
from ..filtering.gh_filter import GH_Filter

from ..model.gateway import Gateway
from ..model.uplink import Uplink

from ..utils.mock import getPoint1Uplinks


class Solver:
    """Solver is the high level class of this lib

        Args:
            compute: string ["auto", "Lsm", "Tdoa", "Toa"]
            filter: array ["timestamp", "result_distance", "gateway_distance"]
            TODO: callable as filter ?
            filter_params {} key: timestamp, distance
            data [] : array of array [lat, long , date, ts]
    """

    # Compute Algorithm
    LSM = "LSM"
    TOA = "TOA"
    TDOA = "TDOA"
    TDOA3D = "TDOA3D"

    # Filter
    DISTANCE = "RESULT"
    TIMESTAMP = "TIMESTAMP"
    GATEWAY = "GATEWAY"

    def __init__(self, kalman_filter, compute="AUTO", filter=["TIMESTAMP", "RESULT", "GATEWAY"], filter_params = {}):
        self.is_resolved = False
        self.compute = compute
        self.filter = filter
        self.filter_params = filter_params
        self.kalman_filter = kalman_filter
        self.last_result = []


    def predict(self, data = []):

        # generate uplink list from data
        uplinks = []
        for item in data[:4]:
            uplinks.append(Uplink(Gateway(item[0], item[1]), item[2], item[3]))

        # Upstream filtering
        if self.TIMESTAMP in self.filter:
            if self.TIMESTAMP in self.filter_params.keys():
                uplinks = filter_uplink_timestamps(uplinks, self.filter_params[self.TIMESTAMP])
            else:
                uplinks = filter_uplink_timestamps(uplinks)

        if self.GATEWAY in self.filter:
            if self.GATEWAY in self.filter_params.keys():
                uplinks = filter_uplink_distance(uplinks, self.filter_params[self.GATEWAY])
            else:
                uplinks = filter_uplink_distance(uplinks)

        # Choose compute algorithm
        if self.compute == self.TDOA:
            self.algorithm = Tdoa(uplinks)
        elif self.compute == self.TOA:
            self.algorithm = Toa(uplinks)
        elif self.compute == self.TDOA3D:
            self.algorithm = Toa3d(uplinks)
        elif self.compute == self.LSM:
            self.algorithm = Lsm(uplinks)
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
            measure = self.algorithm.geolocalized_device.to_array()
            resx, rescov = self.kalman_filter.new_measure(measure)
            print measure[0], measure[1], " <=> ", resx[0], resx[1]
            return resx, measure
        return None

    def _choose_auto_compute(self, params = []):
        if len(params) < 3 :
            raise ValueError("too few value for solving. TODO: search for approximation ? macro geoloc ?")
        elif len(params) == 3:
            self.algorithm = Toa(params)
        elif len(params) == 4:
            self.algorithm = Tdoa(params)
        else:
            self.algorithm = Lsm(params)


if __name__ == '__main__':

    def point1():
        data = getPoint1Uplinks()

        pos = np.array([48.92029793, 2.19017942913])
        dpos = np.array([0., 0.])
        dtime = 1.
        g = .1
        h = .0

        kf = GH_Filter(pos, dpos, dtime, g, h)

        results = np.empty([len(data),2])
        measures = np.empty([len(data),2])
        positions = np.empty([len(data),2])

        solver = Solver(
            kf,
            "TDOA",
            ["TIMESTAMP"],
        )

        for i, x in enumerate(data):
            #  update the filter
            idx = np.random.randint(len(x), size=4)
            res, measure = solver.predict(x[:4])
            # store data to plot
            positions[i] = [48.945997, 2.247975]
            results[i] = res
            measures[i] = measure

        fig, ax = plt.subplots()
        ax.plot(results[:, 0], results[:, 1])
        ax.plot(measures[:,0],measures[:,1], "*")
        ax.plot(positions[:, 0], positions[:, 1],"x")
        plt.show()

    point1()

