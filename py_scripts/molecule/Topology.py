#!/usr/bin/python


"""

	Atom.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from vector3d import *
from PeriodicTable import *
from Atom import *
import string


class Topology:

	"""
	Topology class used to define topologies of atoms
	"""

	def __init__(self):
		self.atoms = []
		self.periodic = PeriodicTable()
		self.residue = ""



	def getAtomIndex(self, name):

		"""
		returns the atom index in the topology tree
		"""

		for i in range(len(self.atoms)):
			if self.atoms[i].name == name:
				return i

		return -1
		
		

	def setResidue(self, res=None):
		
		"""
		sets the current residue to a given residue
		"""

		if res == None:
			return

		self.residue = res



	def newAtom(self):

		"""
		creates a new atom in the topology tree
		"""

		atm = topologyAtom()
		self.atoms.append(atm)
		return atm



	def set13(self):

		"""
		perceives 1-3 bonds
		"""

		for id1 in range(len(self.atoms)):
			atm1 = self.atoms[id1]
			for id2 in range(len(atm1.bonds12)):	
				atm2 = self.atoms[id2]

				for k in range(len(atm2.bonds12)):
					id3 = atm2.bonds12[k]

					if id1 == id3:
						continue

					atm1.bonds13.append(id3)



	def read(self, file=""):

		"""
		reads the topology file format
		"""

		try:
			FILE = open(file, 'r')
		except:
			print "unable to read topology file"
			return

		for line in FILE.readlines():
			line = string.rstrip(line)
			atm = self.newAtom()
			atm.index = int(line[0:3])
			atm.name  = line[5:8]
			atm.element =  line[10:11]


		FILE.close()



	def write(self, file=""):

		"""
		writes the topology file format
		"""

		try:
			FILE = open(file, 'w')
		except:
			print "unable to write topology file"
			return

		self.residue.atom.sort()
		for atm in self.residue.atom:
			# format
			# index - name - element - atomtype - bond12 - bond12 - bond14
			FILE.write('%3i %4s %2s %4s %3i %3i %3i\n' %
				(atm.index, atm.name, atm.element, atm.tree, atm.bnd12, atm.bnd13, atm.bnd14))
		if len(self.residue.rotatable) > 0:
			FILE.write("ROTATABLE:\n")
			for bnd in self.residue.rotatable:
				FILE.write('%3i %3i\n' % (bnd[0], bnd[1]))

		if len(self.residue.ring) > 0:
			FILE.write("RING:\n")
			for bnd in self.residue.ring:
				FILE.write('%3i %3i\n' % (bnd[0], bnd[1]))
		FILE.close()





class topologyAtom(Atom):

	"""
	topology atom class used to store atom info
	"""

	def __init__(self):
		Atom.__init__(self)
		self.index = 0
		self.atomtype = ""
		self.hybrid   = ""
		self.bnd12    = -1
		self.bnd13    = -1
		self.bnd14    = -1
		self.bonds12  = []	
		self.bonds13  = []	
		self.bonds14  = []	
		self.tree     = ""
