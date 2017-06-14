
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sympy

from math import sqrt
from scipy.linalg import block_diag

from filter import Filter
from kalman_filter import kf_filter
from filterpy.kalman import KalmanFilter
from filterpy.kalman import IMMEstimator
from filterpy.common import Q_discrete_white_noise

class imm_filter(Filter):
	def __init__(self, filters, N, mu):
		self.filter = IMMEstimator(filters, mu, M)

	def new_measure(self, measure):
		self.filter.update(measure)
		return self.filter.x.copy, self.filter.x.copy()


# todo

if __name__ == '__main__':

	def car():
		# =========================== CONSTANT ACCELERATION
		dimx = 6
		dimz = 2
		dimNoise = 2
		dt = .1
		correlation = 5 # how fast you want to update model (big number is slow convergercence)
		covariance = 500 # => how close to the measurement you want to be
		# noiseCovariance = 0.1  # => how do you trust your sensor
		noiseCovariance = np.diag([ dt**6/36, dt**5/25,dt**4/16, dt**3/9, dt**2/4, dt**1])

		x = np.array([0., 0., 0., 0., 0., 0.])
		measurementFunc = np.array([[1., 0., 0., 0., 0., 0.],
									[0., 1., 0., 0., 0., 0.]])

		stateTransition = np.array([[1., 0., dt, 0., 0.5*dt**2,        0.],
									[0., 1., 0., dt,        0., 0.5*dt**2],
									[0., 0., 1., 0.,        dt,        0.],
									[0., 0., 0., 1.,        0.,        dt],
									[0., 0., 0., 0.,        1.,        0.],
									[0., 0., 0., 0.,        0.,        1.]])

		kf2 = kf_filter(dimx , dimz, x, covariance, stateTransition, measurementFunc, dt, noiseCovariance, correlation, dimNoise)


		# ========================== CONSTANT SPEED
		dimx = 4
		dimz = 2
		dimNoise = 2
		dt = .1
		correlation = 5 # how fast you want to update model (big number is slow convergercence)
		covariance = 500 # => how close to the measurement you want to be
		# noiseCovariance = 0.1  # => how do you trust your sensor
		noiseCovariance = np.diag([ dt**4/16, dt**3/9, dt**2/4, dt**1])
		x = np.array([0., 0., 0., 0.])
		measurementFunc = np.array([[1., 0., 0., 0.],
									[0., 1., 0., 0.]])
		stateTransition = np.array([[1., 0., dt, 0.],
									[0., 1., 0., dt],
									[0., 0., 1., 0.],
									[0., 0., 0., 1.]])
		kf1 = kf_filter(dimx , dimz, x, covariance, stateTransition, measurementFunc, dt, noiseCovariance, correlation, dimNoise)

		# =========================== MME KALMAN FILTER
		threshold = 10.
		kf = imm_filter(kf1, kf2, threshold)

		# ========================== MEASURE

		epoch = 400
		results = np.empty([epoch, 2])
		# resultscov = np.empty([epoch, 6, 6])
		measures = np.empty([epoch, 2])
		positions = np.empty([epoch, 2])

		for x in xrange(0, epoch):
			noise1 = np.random.rand(2)
			noise2 = np.random.rand(2)
			if x > 3*epoch/4:
				pos = np.array([7*epoch/4 - 2*x, 2*x - 2*epoch])
			elif x > epoch/2:
				pos = np.array([epoch - x, epoch/4 - x])
			elif x > epoch/4:
				pos = np.array([2*x - epoch/2, 3*epoch/4 - 2*x])
			else:
				pos = np.array([x - epoch/4, x])

			measure = pos + 15 * (noise1 - 0.5) + 15 * (noise2 - 0.5)
			#  update the filter
			print x
			resx, rescov = kf.new_measure(measure)
			# store data to plot
			positions[x] = pos
			measures[x] = measure
			results[x] = resx[0:2]
			# resultscov[x] = rescov
		plt.figure(1)
		plt.subplot(221)
		# plt.plot(np.add.reduce(np.add.reduce(resultscov, axis=1), axis=1), label="covariance")
		plt.title("filtre de Kalman order 1")
		plt.subplot(212)
		plt.plot(results[:,0], results[:,1], label="filtre de kalman", markersize=1)
		plt.plot(measures[:,0], measures[:,1], "*", label="mesures", markersize=1)
		plt.plot(positions[:,0], positions[:,1], "x", label="position reele", markersize=1)
		plt.legend(bbox_to_anchor=(.5, .7, .5, 1.),
				   loc=1,
				   ncol=1,
				   mode="expand",
				   borderaxespad=0.)
		plt.show()


	# real main
	# dog()
	car()
	# plain()
