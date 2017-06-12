from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from math import sqrt
import sympy


class kf_filter:
	"""create a gh filter"""
	def __init__(self, dimx, dimz, state, covariance, transitionMat, measurementFunc, dt, noiseCovariance, correlation):
		self.filter = KalmanFilter(dim_x=dimx, dim_z=dimz)
		self.filter.x = np.array(state) 			# state (position and velocity)
		self.filter.F = np.array(transitionMat)  	# state transition matrix
		self.filter.H = np.array(measurementFunc)	# Measurement function
		self.filter.R *= correlation   	            # measurement uncertainty
		
		if np.isscalar(covariance):
		    self.filter.P *= covariance             # covariance matrix 
		else:
		    self.filter.P[:] = covariance      		# [:] makes deep copy
		
		if np.isscalar(noiseCovariance):
		    self.filter.Q = Q_discrete_white_noise(dim=dimx, dt=dt, var=noiseCovariance)
		else:
		    self.filter.Q[:] = noiseCovariance

	def new_measure(self, measure):
		self.filter.predict()
		self.filter.update(measure)
		xs = self.filter.x
		cov = self.filter.P
		return xs, cov



if __name__ == '__main__':

	def dog():
		dimx = 2
		dimz = 1
		dt = .1
		correlation = 5
		covariance = 500
		noiseCovariance = 0.1
		x = np.array([0., 0.])
		measurementFunc = np.array([[1., 0]])
		stateTransition = np.array([[1., dt],
									[0., 1.]])
		kf = kf_filter(dimx , dimz, x, covariance, stateTransition, measurementFunc, dt, noiseCovariance, correlation)

		results = np.array([])
		resultscov = np.array([])
		measures = np.array([])
		positions = np.array([])

		for x in xrange(0, 100):
			noise = np.random.rand(1)[0]
			# noise = np.random.rand(1, 2)
			# pos = np.array([x, x])
			pos = x
			measure = pos + 20 * (noise - 0.5)
			#  update the filter
			resx, rescov  = kf.new_measure(measure)
			# store data to plot
			positions = np.append(positions, pos)
			measures = np.append(measures, measure)
			results = np.append(results, resx[0])
			resultscov = np.append(resultscov, rescov[0])

		plt.figure(1)
		plt.subplot(221)
		plt.plot(resultscov, label="covariance")
		plt.title("filtre de Kalman")
		
		plt.subplot(212)
		plt.plot(results, label="filtre de kalman")
		plt.plot(measures, "*", label="mesures")
		plt.plot(positions, "x", label="position reele")
		plt.legend(bbox_to_anchor=(.5, .7, .5, 1.),
				   loc=1,
				   ncol=1,
				   mode="expand",
				   borderaxespad=0.)
		plt.show()


	def car():
		dimx = 2
		dimz = 1
		dt = .1
		correlation = 5
		covariance = 500
		noiseCovariance = 0.1
		x = np.array([0., 0.])
		measurementFunc = np.array([[1., 0]])
		stateTransition = np.array([[1., dt],
									[0., 1.]])
		kf = kf_filter(dimx , dimz, x, covariance, stateTransition, measurementFunc, dt, noiseCovariance, correlation)

		results = np.array([])
		resultscov = np.array([])
		measures = np.array([])
		positions = np.array([])

		for x in xrange(0, 100):
			noise = np.random.rand(1)[0]
			# noise = np.random.rand(1, 2)
			# pos = np.array([x, x])
			pos = x
			measure = pos + 20 * (noise - 0.5)
			#  update the filter
			resx, rescov  = kf.new_measure(measure)
			# store data to plot
			positions = np.append(positions, pos)
			measures = np.append(measures, measure)
			results = np.append(results, resx[0])
			resultscov = np.append(resultscov, rescov[0])

		plt.figure(1)
		plt.subplot(221)
		plt.plot(resultscov, label="covariance")
		plt.title("filtre de Kalman")
		
		plt.subplot(212)
		plt.plot(results, label="filtre de kalman")
		plt.plot(measures, "*", label="mesures")
		plt.plot(positions, "x", label="position reele")
		plt.legend(bbox_to_anchor=(.5, .7, .5, 1.),
				   loc=1,
				   ncol=1,
				   mode="expand",
				   borderaxespad=0.)
		plt.show()



		# real main
	dog()
	# car()
