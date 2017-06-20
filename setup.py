#from distutils.core import setup
from setuptools import setup
setup(
  name = 'trilateration',
  packages = ['trilateration', 'trilateration.compute', 'trilateration.filtering', 'trilateration.model', 'trilateration.utils'],
  version = '1.0',
  description = 'Finding best intersection or its nearest point for 3 gateways and the distance traveled by the signal for TDOA/TOA trilateration',
  author = 'Royer Robin',
  author_email = 'ktyroby@hotmail.fr',
  url = 'https://github.com/robinroyer/trilateration',
  download_url = 'https://github.com/robinroyer/trilateration/archive/0.1.tar.gz',
  keywords = ['trilateration', 'toa', 'tdoa'],
  classifiers = [],
)
