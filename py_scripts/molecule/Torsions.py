#!/usr/bin/python

"""

	Torsions.py

"""


__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import string, os
from Molecule import *


class Torsions:

	"""
	Torsions class used to calculate torsion angles
	"""


	def __init__(self):
		self.name = ""
		self.torsions = []
		home = os.environ['HOME']
		self.file = home + "/py_scripts/data/torsionDefinitions.dat"



	def readTorsions(self):

		"""
		reads the torsion definitions file
		"""

		try:
			FILE = open(self.file)
		except:
			print "unable to open file:",self.file
			return 0


		cols = []
		tmp  = []
		for line in FILE.readlines():
			cols = string.split(line, "'")
			tmp = string.split(cols[0])

			torsion = TorsionAngle()
			torsion.resname = tmp[0]
			torsion.torname = tmp[1]

			tmp = string.split(cols[1], ";")
			for i in range(4):
				torsion.name[i] = tmp[i]

			tmp = string.split(cols[3], ";")
			for i in range(4):
				torsion.pos[i] = tmp[i]
		
			self.torsions.append(torsion)



	def getTorsion(self, chain=None, resi=None, tor=None):

		"""
		returns the torsion angle for a given residue and torsion type
		"""

		atoms = self.getAtoms(chain, resi, tor)

		if len(atoms) != 4:
			return 0.0

		angle = vector3d.torsion(atoms[0].coord, atoms[1].coord, atoms[2].coord, atoms[3].coord) 
		return angle



	def getAtoms(self, chain=None, resi=None, tor=None):

		"""
		returns the atoms involved in a torsion angle for a given residue and torsion type
		"""

		atoms = []
		residue = chain.getResidue(resi)
		
		if not residue:
			return atoms

		resn = residue.name


		for entry in self.torsions:
			if (entry.resname == resn) and (entry.torname == tor):
				found = True
				for i in range(4):
					curres = int(resi) + int(entry.pos[i])
					currentRes = chain.getResidue(curres)
					
					if not currentRes:
						return atoms

					curratom = currentRes.getAtom(entry.name[i])
					if not curratom:
						return atoms

					atoms.append(curratom)
					

		for entry in self.torsions:
			if (entry.resname == "ALL") and (entry.torname == tor):
				found = True
				for i in range(4):
					curres = int(resi) + int(entry.pos[i])
					currentRes = chain.getResidue(curres)

					if not currentRes:
						return atoms

					curratom = currentRes.getAtom(entry.name[i])
					if not curratom:
						return atoms

					atoms.append(curratom)	


		return atoms




class TorsionAngle:

	"""
	storage class to store information on a torsional angle
	"""

	def __init__(self):
		self.resname = ""
		self.torname = ""
		self.name = [None]*4
		self.pos  = [None]*4

		self.name[0] = ""
		self.name[1] = ""
		self.name[2] = ""
		self.name[3] = ""

		self.pos[0] = 0
		self.pos[1] = 0
		self.pos[2] = 0
		self.pos[3] = 0



	def __repr__(self):

		"""
		prints the torsional angle
		"""

		repr = self.resname + "   " + self.torname + "  '"
		for i in range(4):
			repr += self.name[i]

		repr += "' -> '"

		for i in range(4):
			repr += self.pos[i]

		return repr
