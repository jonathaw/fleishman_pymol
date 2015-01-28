#!/usr/bin/python


"""

        PeriodicTable.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string
import re


class PeriodicTable:

	"""
	class for storing commonly used elements and their associated properties
	"""

	def __init__(self):
	
		self.element_name = []
		self.element_mass = {}
		self.element_radius = {}

		self.populate()



	def populate(self):

		"""
		populates the table
		"""

		self.element_name.append("H"); self.element_mass["H"] = 1.0
		self.element_name.append("C"); self.element_mass["C"] = 12.0
		self.element_name.append("N"); self.element_mass["N"] = 14.0
		self.element_name.append("O"); self.element_mass["O"] = 16.0
		self.element_name.append("S"); self.element_mass["S"] = 32.0
		self.element_name.append("P"); self.element_mass["P"] = 31.0

		# --- rosetta values for the radius --- #
		self.element_radius["H"] = 1.00
		self.element_radius["C"] = 2.00
		self.element_radius["N"] = 1.75
		self.element_radius["O"] = 1.55
		self.element_radius["S"] = 2.00
		self.element_radius["P"] = 1.90



	def determineElement(self, name):

		"""
		determine the element from the atom name
		"""

		c1 = name[0:1]
		c2 = name[1:2]

		for element in self.element_name:
			if c2 == element:
				return c2

		for element in self.element_name:
			if c1 == element:
				return c1

		return ""


