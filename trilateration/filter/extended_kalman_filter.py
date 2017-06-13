from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from math import sqrt
import sympy
from scipy.linalg import block_diag
from filterpy.common import Q_discrete_white_noise

class kf_filter:
	"""create a gh filter"""
	def __init__(self, dimx, dimz, state, covariance, transitionMat, measurementFunc, dt, noiseCovariance, correlation, dimNoise):
		self.filter = KalmanFilter(dim_x=dimx, dim_z=dimz)
		self.filter.x = np.array(state) 			# state (position and velocity)
		self.filter.F = np.array(transitionMat)  	# state transition matrix
		self.filter.H = np.array(measurementFunc)	# Measurement function
		# print correlation.shape
		self.filter.R *= correlation   	            # measurement uncertainty
		
		if np.isscalar(covariance):
		    self.filter.P *= covariance             # covariance matrix 
		else:
		    self.filter.P[:] = covariance      		# [:] makes deep copy
		
		if np.isscalar(noiseCovariance):
		    self.filter.Q = Q_discrete_white_noise(dim=dimNoise, dt=dt, var=noiseCovariance)
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
		dimNoise = 2
		dt = .1
		correlation = 5 # how fast you want to update model (big number is slow convergercence)
		covariance = 500 # => how close to the measurement you want to be
		noiseCovariance = .2 # => how do you trust your sensor
		# x = np.array([0., 0.])
		x = np.array([0., 4000.]) # bad start
		measurementFunc = np.array([[1., 0]])
		stateTransition = np.array([[1., dt],
									[0., 1.]])
		kf = kf_filter(dimx , dimz, x, covariance, stateTransition, measurementFunc, dt, noiseCovariance, correlation, dimNoise)

		results = np.array([])
		resultscov = np.array([])
		measures = np.array([])
		positions = np.array([])

		epoch = 200
		for x in xrange(0, epoch):
			noise1 = np.random.rand(1)
			noise2 = np.random.rand(1)
			# pos = np.array([x, x])
			pos = x
			if x > epoch/2:
				pos = epoch - x
			measure = pos + 20 * (noise1 - 2.5) + 25 * (noise2 + 1.5) # result of 2 gaussians not centered
			#  update the filter
			resx, rescov  = kf.new_measure(measure)
			# print rescov
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
		dimx = 4
		dimz = 2
		dimNoise = 2
		dt = .1
		correlation = 5 # how fast you want to update model (big number is slow convergercence)
		covariance = 5 # => how close to the measurement you want to be
		# noiseCovariance = 0.1  # => how do you trust your sensor
		noiseCovariance = np.diag([ dt**4/16, dt**3/9, dt**2/4, dt**1])
		x = np.array([0., 0., 0., 0.])
		measurementFunc = np.array([[1., 0., 0., 0.],
									[0., 1., 0., 0.]])
		stateTransition = np.array([[1., 0., dt, 0.],
									[0., 1., 0., dt],
									[0., 0., 1., 0.],
									[0., 0., 0., 1.]])
		kf = kf_filter(dimx , dimz, x, covariance, stateTransition, measurementFunc, dt, noiseCovariance, correlation, dimNoise)

		epoch = 500
		results = np.empty([epoch, 4])
		resultscov = np.empty([epoch, 4, 4])
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

			measure = pos + 20 * (noise1 - 0.7) + 25 * (noise2 - 0.3)
			#  update the filter
			resx, rescov = kf.new_measure(measure)
			# store data to plot
			positions[x] = pos
			measures[x] = measure
			results[x] = resx
			resultscov[x] = rescov
		plt.figure(1)
		plt.subplot(221)
		plt.plot(np.add.reduce(np.add.reduce(resultscov, axis=1), axis=1), label="covariance")
		plt.title("filtre de Kalman")
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

	def plain():
		dimx = 6
		dimz = 2
		dimNoise = 2
		dt = .1
		correlation = 5 # how fast you want to update model (big number is slow convergercence)
		covariance = 5 # => how close to the measurement you want to be
		# noiseCovariance = 0.1  # => how do you trust your sensor
		# noiseCovariance = np.diag([ dt**4/16, dt**3/9, dt**2/4, dt**1])
		noiseCovariance = Q_discrete_white_noise(dim=2, dt=dt, var=0.01)
		noiseCovariance = block_diag(q, q, q)


		x = np.array([0., 0., 0., 0.])
		measurementFunc = np.array([[1., 0., 0., 0., 0., 0.],
									[0., 1., 0., 0., 0., 0.]])

		stateTransition = np.array([[1., 0., dt, 0., 0.5*dt**2,        0.],
									[0., 1., 0., dt,        0., 0.5*dt**2],
									[0., 0., 1., 0.,        dt,        0.],
									[0., 0., 0., 1.,        0.,        dt],
									[0., 0., 0., 0.,        1.,        0.],
									[0., 0., 0., 0.,        0.,        1.]])

		kf = kf_filter(dimx , dimz, x, covariance, stateTransition, measurementFunc, dt, noiseCovariance, correlation, dimNoise)

		epoch = 500
		results = np.empty([epoch, 4])
		resultscov = np.empty([epoch, 4, 4])
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

			measure = pos + 20 * (noise1 - 0.7) + 25 * (noise2 - 0.3)
			#  update the filter
			resx, rescov = kf.new_measure(measure)
			# store data to plot
			positions[x] = pos
			measures[x] = measure
			results[x] = resx
			resultscov[x] = rescov
		plt.figure(1)
		plt.subplot(221)
		plt.plot(np.add.reduce(np.add.reduce(resultscov, axis=1), axis=1), label="covariance")
		plt.title("filtre de Kalman")
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
	#dog()
	car()
	plain()
