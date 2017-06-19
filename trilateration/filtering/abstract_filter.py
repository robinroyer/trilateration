from __future__ import absolute_import

from abc import ABCMeta, abstractmethod

class Filter(object):

	def new_measure(self, measure):
		raise NotImplementedError('subclasses must override foo()!')
