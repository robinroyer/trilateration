from filterpy.kalman import ExtendedKalmanFilter
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy.random import randn
from math import sqrt
import sympy


class RadarSim(object):
    """ Simulates the radar signal returns from an object
    flying at a constant altityude and velocity in 1D. 
    """
    
    def __init__(self, dt, pos, vel, alt):
        self.pos = pos
        self.vel = vel
        self.alt = alt
        self.dt = dt
        
    def get_range(self):
        """ Returns slant range to the object. Call once 
        for each new measurement at dt time from last call.
        """
        
        # add some process noise to the system
        self.vel = self.vel  + .1*randn()
        self.alt = self.alt + .1*randn()
        self.pos = self.pos + self.vel*self.dt
    
        # add measurement noise
        err = self.pos * 0.05*randn()
        slant_dist = math.sqrt(self.pos**2 + self.alt**2)
        
        return slant_dist + err


class ekf_filter:
	"""create a gh filter"""
	def __init__(self, dimx, x, dimz, f):
		self.filter = ExtendedKalmanFilter(dim_x=dimx, dim_z=dimz)
		self.filter.x = x
		self.filter.F = f

	def HJacobian_at(x):
    """ compute Jacobian of H matrix at x """
    horiz_dist = x[0]
    altitude   = x[2]
    denom = sqrt(horiz_dist**2 + altitude**2)
    return array ([[horiz_dist/denom, 0., altitude/denom]])

	def hx(x):
	    """ compute measurement for slant range that
	    would correspond to state x.
	    """
	    
	    return (x[0]**2 + x[2]**2) ** 0.5

	def new_measure(self, measure, hjacob, hx):
		self.filter.update(measure, hjacob, hx)
		return self.filter.predict()

if __name__ == '__main__':
	pos = np.array([0.,0.])
	dpos = np.array([1.,1.])
	dtime = 1.
	g = .1
	h = .0

	filter = gh_filter(pos, dpos, dtime, g, h)

	results = np.array([])
	measures = np.array([])
	positions = np.array([])

	for x in xrange(0, 80):
		noise = np.random.rand(1, 2)
		pos = np.array([x, x])
		measure = pos + 20 * (noise - 0.5)
		#  update the filter
		res = filter.new_measure(measure)
		# store data to plot
		positions = np.append(positions, pos)
		measures = np.append(measures, measure)
		results = np.append(results, res[0])

	fig, ax = plt.subplots()
	ax.plot(results)
	ax.plot(measures, "*")
	ax.plot(positions, "x")
	plt.show()
