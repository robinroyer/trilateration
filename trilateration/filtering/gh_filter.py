from __future__ import absolute_import

import numpy as np
import matplotlib.pyplot as plt
from filterpy.gh import GHFilter

from ..filtering.abstract_filter import Filter


class GH_Filter(Filter):
	"""create a gh filter"""
	def __init__(self, pos, dpos, dtime, g, h):
		self.g = g
		self.h = h
		self.filter = GHFilter(x=pos, dx=dpos, dt=dtime, g=g, h=h)

	def new_measure(self, measure, g=None, h=None):
		if g is not None:
			self.g = g
		if h is not None:
			self.h = h

		return self.filter.update(measure, self.g, self.h)

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
