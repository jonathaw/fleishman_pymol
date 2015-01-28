#!/usr/bin/python


__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string
from Constraint import *

class Cstfile:

	"""
	container class for enzyme constraints
	"""


	def __init__(self):

		self.constraints = []



	def newConstraint(self):

		"""
		creates a new constraint
		"""

		cst = Constraint()
		self.constraints.append(cst)

		return cst



	def addConstraint(self, cst):

		"""
		adds a constraint to the cstfile
		"""

		self.constraints.append(cst)


	def numConstraints(self):

		"""
		returns the number of constraints
		"""

		return len(self.constraints)


	
	def read(self):
		
		"""
		reads in a constraint file
		"""

		pass



	def write(self):

		"""
		writes out a constraint file
		"""

		pass
