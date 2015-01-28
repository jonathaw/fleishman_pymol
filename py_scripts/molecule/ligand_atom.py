#!/usr/bin/python

"""

	ligand.py

"""


__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from Atom import *

class ligand_atom(Atom):
	
	def __init__(self):
		Atom.__init__(self)
		self.index = -9
		self.ring  = 0
		self.tree  = ""
		self.bonds = []
		self.bnd12 = -9
		self.bnd13 = -9
		self.bnd14 = -9
		self.atomtype = "A"

	def __cmp__(self, other):
		return cmp(self.index, other.index)
