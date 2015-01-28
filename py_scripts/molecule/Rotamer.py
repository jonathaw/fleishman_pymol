#!/usr/bin/python

"""

	Rotamer.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


class Rotamer:

	"""
	class for representing rotamers
	"""

	def __init__(self):	
		self.index  = 0
		self.seqpos = 0
		self.aatype = 0
		self.state  = 0

		self.phi  = 0.0
		self.psi  = 0.0

		self.chi1 = 0.0
		self.chi2 = 0.0
		self.chi3 = 0.0
		self.chi4 = 0.0

		self.stdev1 = 0.0
		self.stdev2 = 0.0
		self.stdev3 = 0.0
		self.stdev4 = 0.0


	def clone(self, rhs):

		"""
		clones self
		"""

		rhs.index = self.index
		rhs.seqpos = self.seqpos
		rhs.aatype = self.aatype
		rhs.state = self.state

		rhs.phi = self.phi
		rhs.psi = self.psi

		rhs.chi1 = self.chi1
		rhs.chi2 = self.chi2
		rhs.chi3 = self.chi3
		rhs.chi4 = self.chi4

		rhs.stdev1 = self.stdev1
		rhs.stdev2 = self.stdev2
		rhs.stdev3 = self.stdev3
		rhs.stdev4 = self.stdev4


	def matches(self, phi=0.0, psi=0.0, chi1=0.0, chi2=0.0, chi3=0.0, chi4=0.0):

		"""
		does a rotamer match up with a given set of chi angles
		"""

		if abs(phi-self.phi) > 0.1 or abs(psi-self.psi) > 0.1:
			return False

		if chi1 < (self.chi1 - self.stdev1) or chi1 > (self.chi1 + self.stdev1):
			return False


		if chi2 < (self.chi2 - self.stdev2) or chi2 > (self.chi2 + self.stdev2):
			return False


		if chi3 < (self.chi3 - self.stdev3) or chi3 > (self.chi3 + self.stdev3):
			return False


		if chi4 < (self.chi4 - self.stdev4) or chi4 > (self.chi4 + self.stdev4):
			return False

		return True


	def matchesRot(self, rhs):

		"""
		does a rotamer match up with another rotamer (identity and angles)
		"""
		
		if abs(self.chi1-rhs.chi1) > 0.1:
			return False
		if abs(self.chi2-rhs.chi2) > 0.1:
			return False
		if abs(self.chi3-rhs.chi3) > 0.1:
			return False
		if abs(self.chi4-rhs.chi4) > 0.1:
			return False

		return True



	def display(self):
		
		"""
		print out the rotamer
		"""
		
		print self.phi,self.psi,self.chi1,self.chi2,self.chi3,self.chi4
