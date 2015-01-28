#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

class ResidueProperties:

	"""
	class used to store properties of amino acids
	"""

	def __init__(self):
		self.polar = ["ASN", "GLN", "CYS", "HIS", "SER", "THR"]
		self.nonpolar = ["ALA", "VAL", "LEU", "ILE", "PRO", "GLY", "MET"]
		self.charged = ["GLU", "ASP", "ARG", "LYS"]
		self.aromatic = ["PHE", "TYR", "TRP"]

		self.polar1    = ["N", "Q", "C", "H", "S", "T"]
		self.nonpolar1 = ["A", "V", "L", "I", "P", "G", "M"]
		self.charged1  = ["E", "D", "R", "K"]
		self.aromatic1 = ["F", "Y", "W"]



	def isPolar(self, res=None, code=""):

		"""
		checks to see if a residue is polar
		"""

		if res != None:
			rn = res.name
			if rn in self.polar:
				return True
		elif code != "":
			if code in self.polar1:
				return True

		return False
				
	

	def isNonPolar(self,res=None, code=""):

		"""
		checks to see if a residue is non polar
		"""

		if res != None:
			rn = res.name
			if rn in self.nonpolar:
				return True
		elif code != "":
			if code in self.nonpolar1:
				return True

		return False



	def isCharged(self,res=None, code=""):
		
		"""
		checks to see if a residue is charged
		"""

		if res != None:
			rn = res.name
			if rn in self.charged:
				return True
		elif code != "":
			if code in self.charged1:
				return True

		return False



	def isAromatic(self,res=None, code=""):
		
		"""
		checks to see if a residue is aromatic
		"""

		if res != None:
			rn = res.name
			if rn in self.aromatic:
				return True
		elif code != None:
			if code in self.aromatic1:
				return True

		return False
