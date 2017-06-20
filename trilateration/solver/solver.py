from __future__ import absolute_import

import time
import datetime
import string
import numpy as np
import matplotlib.pyplot as plt

from ..compute.lsm import Lsm
from ..compute.tdoa import Tdoa
from ..compute.tdoa3d import Tdoa3d
from ..compute.toa import Toa

from ..filtering.statistic_filter import filter_point_distance, filter_uplink_timestamps, filter_uplink_distance
from ..filtering.mme_kalman_filter import MME_Filter
from ..filtering.kalman_filter import KF_Filter

from ..model.gateway import Gateway
from ..model.uplink import Uplink
from ..model.point import Point

from ..utils.mock import getPoint1Uplinks, getPoint2Uplinks, getPoint3Uplinks, getPoint4Uplinks, getPoint5Uplinks, getMob1Uplinks, getMob2Uplinks, measure_mob1, measure_mob2


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
        for item in data:
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
        intersections = []
        if self.compute == self.TDOA:
            for i in xrange(len(uplinks) - 3):
                self.algorithm = Tdoa(uplinks[i:i+4])
                intersections.append(self.algorithm._intersections[0])
        elif self.compute == self.TOA:
            self.algorithm = Toa(uplinks)
        elif self.compute == self.TDOA3D:
            self.algorithm = Toa3d(uplinks)
        elif self.compute == self.LSM:
            self.algorithm = Lsm(uplinks)
        else:
            self._choose_auto_compute(uplinks)
        # Downstream filtering
        if self.DISTANCE in self.filter and len(intersections) > 1:
            if self.DISTANCE in self.filter_params.keys():
                solutions = filter_point_distance(intersections, self.filter_params[self.DISTANCE])
            else:
                solutions = filter_point_distance(intersections)

            mean_lat, mean_lon = .0, .0
            for intersection in solutions:
                mean_lat += intersection.lat
                mean_lon += intersection.lon

            mean_lat /= float(len(solutions))
            mean_lon /= float(len(solutions))

            measure = [mean_lat, mean_lon]
            resx, rescov = self.kalman_filter.new_measure(measure)
            self.is_resolved = True
            return resx, measure

        elif self.algorithm.is_resolved:
            self.is_resolved = True
            measure = self.algorithm.geolocalized_device.to_array()
            resx, rescov = self.kalman_filter.new_measure(measure)
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


class TdoaSolver:
    """Solver is the high level class of this lib

        Args:
            filter: array ["timestamp", "result_distance", "gateway_distance"]
            TODO: callable as filter ?
            filter_params {} key: timestamp, distance
            data [] : array of array [lat, long , date, ts]
    """

    # Filter
    RESULT = "RESULT"
    TIMESTAMP = "TIMESTAMP"
    GATEWAY = "GATEWAY"

    def __init__(self, filter=["TIMESTAMP", "RESULT", "GATEWAY"], filter_params = {"TIMESTAMP": 2, "RESULT": 2, "GATEWAY": 2}):
        self.is_resolved = False
        self.filter = filter
        self.filter_params = filter_params
        self.kalman_filter = None
        self.last_result = None

    def predict(self, data = []):

        # generate uplink list from data
        uplinks = []
        for item in data:
            uplinks.append(Uplink(Gateway(item[0], item[1]), item[2], item[3]))
        # filtering timestamp
        uplinks = filter_uplink_timestamps(uplinks, self.filter_params[self.TIMESTAMP])
        uplinks = filter_uplink_distance(uplinks, self.filter_params[self.GATEWAY])

        # Compute
        intersections = []
        for i in xrange(len(uplinks) - 3):
            tdoa = Tdoa(uplinks[i:i+4])
            intersections.append(tdoa._intersections[0])

        # filtering result
        solutions = filter_point_distance(intersections, self.filter_params[self.RESULT])
        # mean
        measure = reduce(lambda acc, x: [acc[0] + x.lat, acc[1] + x.lon], solutions, [0., 0.])
        if len(solutions) == 0:
            raise Exception('Computation error, we have no solutions')     
        measure = [measure[0] / len(solutions), measure[1] / len(solutions)]
        # init the kalman filter
        if self.kalman_filter is None:
            # =========================== CONSTANT ACCELERATION
            dimx = 6
            dimz = 2
            dimNoise = 2
            dt = 30.
            correlation = 5000000000 # how fast you want to update model (big number is slow convergercence)
            covariance = .0000005 # => how close to the measurement you want to be
            # noiseCovariance = 0.1  # => how do you trust your sensor
            noiseCovariance = np.diag([ dt**6/36, dt**5/25,dt**4/16, dt**3/9, dt**2/4, dt**1])

            x = np.array([measure[0], measure[1], 0., 0., 0., 0.])
            measurementFunc = np.array([[1., 0., 0., 0., 0., 0.],
                                        [0., 1., 0., 0., 0., 0.]])

            stateTransition = np.array([[1., 0., dt, 0., .5*dt**2,       0.],
                                        [0., 1., 0., dt,       0., .5*dt**2],
                                        [0., 0., 1., 0.,       dt,       0.],
                                        [0., 0., 0., 1.,       0.,       dt],
                                        [0., 0., 0., 0.,       1.,       0.],
                                        [0., 0., 0., 0.,       0.,       1.]])

            kf2 = KF_Filter(dimx , dimz, x, covariance, stateTransition, measurementFunc, dt, noiseCovariance, correlation, dimNoise)


            # ========================== CONSTANT SPEED
            dimx = 4
            dimz = 2
            dimNoise = 2
            dt = 30.
            correlation = 5000000000 # how fast you want to update model (big number is slow convergercence)
            covariance = .000000005 # => how close to the measurement you want to be
            # noiseCovariance = 0.1  # => how do you trust your sensor
            noiseCovariance = np.diag([ dt**4/16, dt**3/9, dt**2/4, dt**1])
            x = np.array([measure[0], measure[1], 0., 0.])
            measurementFunc = np.array([[1., 0., 0., 0.],
                                        [0., 1., 0., 0.]])
            stateTransition = np.array([[1., 0., dt, 0.],
                                        [0., 1., 0., dt],
                                        [0., 0., 1., 0.],
                                        [0., 0., 0., 1.]])
            kf1 = KF_Filter(dimx , dimz, x, covariance, stateTransition, measurementFunc, dt, noiseCovariance, correlation, dimNoise)

            # =========================== MME KALMAN FILTER
            threshold = 2.
            self.kalman_filter = MME_Filter(kf1, kf2, threshold)

        resx, rescov = self.kalman_filter.new_measure(measure)
        self.is_resolved = True
        self.last_result = Point(resx[0], resx[1])
        return resx, measure


if __name__ == '__main__':

    def point1():
        data = getPoint1Uplinks()

        results = []
        measures = []
        positions = []
        distance = []

        solver = TdoaSolver(
            ["TIMESTAMP", "RESULT"],
            filter_params={
                "TIMESTAMP": 1.5,
                "RESULT": .5,
                "GATEWAY": 4.,
            }
        )
                
        for x in data:
            try:
                res, measure = solver.predict(x)
            except Exception as e:
                print e
                continue
            # store data to plot
            positions.append([48.945997, 2.247975])
            results.append(res[0:2])
            measures.append(measure)
            distance.append(Point(48.945997, 2.247975).distance_from_point(Point(res[0], res[1])))

        plt.subplot(221)
        plt.plot(np.array(results)[:, 0], np.array(results)[:, 1])
        plt.plot(np.array(measures)[:, 0], np.array(measures)[:, 1], "*")
        plt.plot(np.array(positions)[:, 0], np.array(positions)[:, 1],"x")
        plt.subplot(212)
        plt.plot(distance)
        plt.show()

    def point2():
        data = getPoint2Uplinks()

        results = []
        measures = []
        positions = []
        distance = []

        solver = TdoaSolver(
            ["TIMESTAMP", "RESULT"],
            filter_params={
                "TIMESTAMP": 2.5,
                "RESULT": .7,
                "GATEWAY": 4.,
            }
        )
                
        for x in data:
            try:
                res, measure = solver.predict(x)
            except Exception as e:
                print e
                continue

            # store data to plot
            positions.append([48.941673, 2.229437])
            results.append(res[0:2])
            measures.append(measure)
            distance.append(Point(48.941673, 2.229437).distance_from_point(Point(res[0], res[1])))

        plt.subplot(221)
        plt.plot(np.array(results)[:, 0], np.array(results)[:, 1])
        plt.plot(np.array(measures)[:, 0], np.array(measures)[:, 1], "*")
        plt.plot(np.array(positions)[:, 0], np.array(positions)[:, 1],"x")
        plt.subplot(212)
        plt.plot(distance)
        plt.show()

    def point3():
        data = getPoint3Uplinks()

        results = []
        measures = []
        positions = []
        distance = []

        solver = TdoaSolver(
            ["TIMESTAMP", "RESULT"],
            filter_params={
                "TIMESTAMP": 1.5,
                "RESULT": .5,
                "GATEWAY": 4.,
            }
        )
                
        for x in data:
            try:
                res, measure = solver.predict(x)
            except Exception as e:
                print e
                continue
            # store data to plot
            positions.append([48.950176, 2.230886])
            results.append(res[0:2])
            measures.append(measure)
            distance.append(Point(48.950176, 2.230886).distance_from_point(Point(res[0], res[1])))

        plt.subplot(221)
        plt.plot(np.array(results)[:, 0], np.array(results)[:, 1])
        plt.plot(np.array(measures)[:, 0], np.array(measures)[:, 1], "*")
        plt.plot(np.array(positions)[:, 0], np.array(positions)[:, 1],"x")
        plt.subplot(212)
        plt.plot(distance)
        plt.show()

    def point4():
        data = getPoint4Uplinks()

        results = []
        measures = []
        positions = []
        distance = []

        solver = TdoaSolver(
            ["TIMESTAMP", "RESULT"],
            filter_params={
                "TIMESTAMP": 1.5,
                "RESULT": .5,
                "GATEWAY": 4.,
            }
        )
                
        for x in data:
            try:
                res, measure = solver.predict(x)
            except Exception as e:
                print e
                continue
            # store data to plot
            positions.append([48.942036, 2.209877])
            results.append(res[0:2])
            measures.append(measure)
            distance.append(Point(48.942036, 2.209877).distance_from_point(Point(res[0], res[1])))

        plt.subplot(221)
        plt.plot(np.array(results)[:, 0], np.array(results)[:, 1])
        plt.plot(np.array(measures)[:, 0], np.array(measures)[:, 1], "*")
        plt.plot(np.array(positions)[:, 0], np.array(positions)[:, 1],"x")
        plt.subplot(212)
        plt.plot(distance)
        plt.show()

    def point5():
        data = getPoint5Uplinks()

        results = []
        measures = []
        positions = []
        distance = []

        solver = TdoaSolver(
            ["TIMESTAMP", "RESULT"],
            filter_params={
                "TIMESTAMP": 1.5,
                "RESULT": 1.5,
                "GATEWAY": 4.,
            }
        )
                
        for x in data:
            try:
                res, measure = solver.predict(x)
            except Exception as e:
                print e
                continue
            # store data to plot
            positions.append([48.942760, 2.213429])
            results.append(res[0:2])
            measures.append(measure)
            distance.append(Point(48.942760, 2.213429).distance_from_point(Point(res[0], res[1])))

        plt.subplot(221)
        plt.plot(np.array(results)[:, 0], np.array(results)[:, 1])
        plt.plot(np.array(measures)[:, 0], np.array(measures)[:, 1], "*")
        plt.plot(np.array(positions)[:, 0], np.array(positions)[:, 1],"x")
        plt.subplot(212)
        plt.plot(distance)
        plt.show()

    def mob1():
        data = getMob1Uplinks()

        results = []
        measures = []
        positions = []
        distance = []

        solver = TdoaSolver(
            ["TIMESTAMP", "RESULT"],
            filter_params={
                "TIMESTAMP": 1.5,
                "RESULT": 1.5,
                "GATEWAY": 4.,
            }
        )
                
        for i, x in enumerate(data):
            try:
                res, measure = solver.predict(x)
            except Exception as e:
                print e
                continue
            # store data to plot
            positions.append(measure_mob1[i])
            results.append(res[0:2])
            measures.append(measure)
            distance.append(Point(48.942760, 2.213429).distance_from_point(Point(res[0], res[1])))

        plt.subplot(221)
        plt.plot(np.array(results)[:, 0], np.array(results)[:, 1])
        plt.plot(np.array(measures)[:, 0], np.array(measures)[:, 1], "*")
        plt.plot(np.array(positions)[:, 0], np.array(positions)[:, 1],"x")
        plt.subplot(212)
        plt.plot(distance)
        plt.show()

    def mob2():
        data = getMob2Uplinks()

        results = []
        measures = []
        positions = []
        distance = []

        solver = TdoaSolver(
            ["TIMESTAMP", "RESULT"],
            filter_params={
                "TIMESTAMP": 1.5,
                "RESULT": 1.5,
                "GATEWAY": 4.,
            }
        )
                
        for i, x in enumerate(data):
            try:
                res, measure = solver.predict(x)
            except Exception as e:
                print e
                continue
            # store data to plot
            positions.append(measure_mob2[i])
            results.append(res[0:2])
            measures.append(measure)
            distance.append(Point(48.942760, 2.213429).distance_from_point(Point(res[0], res[1])))

        plt.subplot(221)
        plt.plot(np.array(results)[:, 0], np.array(results)[:, 1])
        plt.plot(np.array(measures)[:, 0], np.array(measures)[:, 1], "*")
        plt.plot(np.array(positions)[:, 0], np.array(positions)[:, 1],"x")
        plt.subplot(212)
        plt.plot(distance)
        plt.show()

    # point1()
    # point2()
    # point3()
    # point4()
    # point5()
    mob1()
    mob2()
