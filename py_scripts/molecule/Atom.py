#!/usr/bin/python


"""

	Atom.py

	An atom is the basic building block for our molecule classes

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from vector3d import *


class Atom:


	def __init__(self, residue=None, name="XXXX", file_id=0, x=0.0, y=0.0, z=0.0):
		self.parentResidue = residue
		self.name      = name
		self.file_id   = file_id
		self.coord     = vector3d(x, y, z)
		self.element   = ""
		self.chain     = " "
		self.local     = " "
		self.mass      = 0
		self.bfactor   = 0.0
		self.occupancy = 1.0
		self.atomType  = ""
		self.kind      = "ATOM  "
		self.chsymbol  = "  "
		self.resn      = "XXX"
		self.resi      = 0
		self.rest      = ""
		self.radius    = 0



	def display(self):
		
		"""
		returns a string containing atom information
		"""

		repr = ('%6s %4i %4s %3s %1s%4i    %8.3f%8.3f%8.3f%6.2f%6.2f' %
						(self.kind, int(self.file_id), self.name, self.resn, self.chain,int(self.resi),
						self.coord.x, self.coord.y, self.coord.z, self.occupancy, self.bfactor))

		return repr


	def __repr__(self):

		"""
		prints the atom information
		"""
	
		repr = self.display()
		return repr



	def copy(self, cpatom):

		"""
		function copy: provides a deep copy of the atom class
		"""

		cpatom.file_id   = self.file_id
		cpatom.name      = self.name

		cpatom.coord.x  = self.coord.x
		cpatom.coord.y  = self.coord.y
		cpatom.coord.z  = self.coord.z

		cpatom.element   = self.element
		cpatom.chain     = self.chain
		cpatom.mass      = self.mass
		cpatom.bfactor   = self.bfactor
		cpatom.occupancy = self.occupancy
		cpatom.atomType  = self.atomType
		cpatom.kind      = self.kind
		cpatom.chsymbol  = self.chsymbol
		cpatom.rest      = self.rest
		cpatom.local     = self.local



	def clone(self):

		"""
		function clone: returns a replica of the current atom
		"""

		replica = Atom()
		self.copy(replica)
		return replica



	def translate(self, vector):

		"""
		function translate: translates an atom coordinates by a given vector
		"""

		self.coord += vector
		


	def distance(self, rhs):

		"""
		function distance: returns the distance betweeen the coordinates
		of two atoms
		"""

		return self.coord.distance(rhs.coord)


	def dist2(self, rhs):

		"""
		function dist2: returns the square of the distance between the coordinates
		of two atoms
		"""

		return self.coord.dist2(rhs.coord)



