#!/usr/bin/python


__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import string

class Constraint:

	"""
	class used for enzyme constraints
	"""


	def __init__(self):

		self.templateA = cst_template()
		self.templateB = cst_template()
		self.distanceAB = dist_cst()
		print self.distanceAB



class cst_template:

	"""
	class used for constraint templates
	"""

	def __init__(self):
		
		self.atom_ids  = []
		self.atom_name = ""
		self.seqpos    = 0
		self.residue3  = ""
		self.residue1  = ""



class dist_cst:

	"""
	distance constraint
	"""

	def __init__(self):

		self.name   = "distanceAB:"
		self.r      = 0.0
		self.delta  = 0.0
		self.weight = 0.0
		self.cov    = 0


	def __repr__(self):

		repr = "CONSTRAINT:: %-9s: %6.2f%6.2f%6.2f%i3" % (self.name,self.r,self.delta,self.weight,self.cov)
		return repr

