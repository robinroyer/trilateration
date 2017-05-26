
import time
import datetime
import numpy as np

from trilateration.model.point import point
from trilateration.model.uplink import uplink
from trilateration.model.gateway import gateway

def filter_uplink_timestamps(uplinks, m=2):
    """Statical fitler on Timestamp distribution

        Args:
            uplinks: List of uplink to filter
            m: multiplicator of std to filter x < m * std

        Return:
            The list of uplink filtered on the timestamp
    """
    data = np.array([])
    for uplink in uplinks:
        data = np.append(data, uplink.timestamp)

    mean = np.mean(data)
    std = np.std(data)
    return filter(lambda u: abs(u.timestamp - mean) < m * std, uplinks)


def filter_point_distance(points, m=2):
    """Statical fitler on points distance distribution

        Args:
            points: List of point to filter
            m: multiplicator of std to filter x < m * std

        Return:
            The list of point filtered on the distance distribution
    """
    data = np.empty([len(points), 2])
    for i, p in enumerate(points):
        data[i,0] = p.lat
        data[i,1] = p.lon

    mean = np.mean(data, axis=0)
    mean_point = point(mean[0], mean[1])

    std = np.std(data, axis=0)
    std_point = point(std[0], std[1])

    return filter(lambda p: (abs(p.lat - mean_point.lat) < m * std_point.lat) and abs(p.lon - mean_point.lon) < m * std_point.lon, points)


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

