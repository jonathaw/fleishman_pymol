#!/usr/bin/python


"""

	NMRresidue.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from NMRatom import *

class NMRresidue:

	"""
	storage class for NMRatoms
	"""

	def __init__(self):
		self.id   = 0
		self.name = ""
		self.atom = []


	def numAtoms(self):

		"""
		returns the number of atoms in a given residue
		"""

		return len(self.atom)


	def addAtom(self, atm):

		"""
		adds an atom to the NMR residue
		"""

		self.atom.append(atm)	


	def newAtom(self):

		"""
		creates and returns a new atom in the residue
		"""

		atm = NMRatom()
		self.addAtom(atm)
		return atm


	def getAtom(self,name):

		"""
		returns an atom of given name
		"""

		for atom in self.atom:
			if atom.name == name:
				return atom

		return None


	def atomExists(self,name):

		"""
		checks to see whether an atom of given name exists
		"""

		for atom in self.atom:
			if atom.name == name:
				return True

		return False


	def removeAtom(self,name):

		"""
		removes an atom of given name
		"""

		for atom in self.atom:
			if atom.name == name:
				self.atom.remove(atom)


