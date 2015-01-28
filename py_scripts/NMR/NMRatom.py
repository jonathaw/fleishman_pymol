#!/usr/bin/python


"""

	NMRatom.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


class NMRatom:

	"""
	class used for storing NMR information for a given atom
	"""

	def __init__(self):
		self.name     = ""
		self.resi     = 0
		self.cs_value = 0
		self.cs_stdev = 0

