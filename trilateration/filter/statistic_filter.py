
import time
import datetime
import numpy as np

from ..model.point import point
from ..model.uplink import uplink
from ..model.gateway import gateway

def filter_uplink_timestamps(uplinks, m=2):
    """Statical fitler on Timestamp distribution

        Args:
            uplinks: List of uplink to filter
            m: multiplicator of std to filter x < m * std

        Return:
            The list of uplink filtered on the timestamp
    """
    if len(uplinks) == 0:
        return []
    if m < 0:
        m = 1
    data = np.empty([len(uplinks), 2], dtype=object)
    for i, uplink in enumerate(uplinks):
        temp = 0
        for uplk in uplinks:
            temp += uplink.timestamp - uplk.timestamp
        data[i, 0] = uplink
        data[i, 1] = temp

    mean = np.mean(data[:,1])
    std = np.std(data[:,1])
    # apply filtering by row
    check_outliner = lambda d: abs(d[1] - mean) <= m * std
    bool_arr = np.array([check_outliner(row) for row in data])
    return data[bool_arr][:, 0]


def filter_point_distance(points, m=2):
    """Statical fitler on points distance distribution

        Args:
            points: List of point to filter
            m: multiplicator of std to filter x < m * std

        Return:
            The list of point filtered on the distance distribution
    """
    if len(points) == 0:
        return []
    if m < 0:
        m = 1
    data = np.empty([len(points), 2], dtype=object)
    for i, point in enumerate(points):
        temp = 0
        for p in points:
            temp += point.distance_from_point(p)
        data[i,0] = point
        data[i,1] = temp

    mean = np.mean(data[:,1])
    std = np.std(data[:,1])

    # apply filtering by row
    check_outliner = lambda p: abs(p[1] - mean) <= m * std
    bool_arr = np.array([check_outliner(row) for row in data])
    return data[bool_arr][:, 0]

def filter_uplink_distance(uplinks, m=2):
    """Statical fitler on uplinks distance distribution

        Args:
            uplinks: List of point to filter
            m: multiplicator of std to filter x < m * std

        Return:
            The list of point filtered on the distance distribution
    """
    if len(uplinks) == 0:
        return []
    if m < 0:
        m = 1
    data = np.empty([len(uplinks), 2], dtype=object)
    for i, uplink in enumerate(uplinks):
        temp = 0
        for u in uplinks:
            temp += uplink.gateway.distance_from_point(u.gateway)
        data[i,0] = uplink.gateway
        data[i,1] = temp

    mean = np.mean(data[:,1])
    std = np.std(data[:,1])

    # apply filtering by row
    check_outliner = lambda p: abs(p[1] - mean) <= m * std
    bool_arr = np.array([check_outliner(row) for row in data])
    return data[bool_arr][:, 0]


if __name__ == '__main__':

    # uplinks = []
    # for i in xrange(0,10):
    #     g = gateway(48.84, 2.26)
    #     d = datetime.datetime.now()
    #     t = int(time.time() * 1000000000)  
    #     uplinks.append(uplink(g, d, t))

    # uplinks[2].timestamp = int(time.time() * 1000000000)  + 4000000

    # print len(uplinks)
    # res =  filter_uplink_timestamps(uplinks, 2.5)
    # print len(res)

    points = []
    for i in xrange(0,10):
        points.append(point(48.84 + i, 2.26 + i))
    print len(points)
    res =  filter_point_distance(points, 1)
    print len(res)

