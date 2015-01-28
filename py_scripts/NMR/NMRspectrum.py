#!/usr/bin/python


"""

	NMRspectrum.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from NMRresidue import *
import string

class NMRspectrum:

	"""
	storage class for NMRresidues
	"""

	def __init__(self):
		self.id      = 0
		self.residue = []


	
	def numResidues(self):

		"""
		returns the number of residues in the spectrum
		"""

		return len(self.residue)


	def addResidue(self, res):

		"""
		adds a residue to the spectrum
		"""

		self.residue.append(res)	


	
	def newResidue(self):

		"""
		creates and returns a new residue in the spectrum
		"""

		res = NMRresidue()
		self.addResidue(res)
		return res


	
	def getResidue(self,id):

		"""
		returns a residue of given id
		"""

		for residue in self.residue:
			if residue.id == id:
				return residue

		return None


	def residueExists(self,id):

		"""
		checks to see whether a residue of given id exists
		"""

		for residue in self.residue:
			if residue.id == id:
				return True

		return False


	def removeResidue(self,name):

		"""
		removes a residue of given name
		"""

		for residue in self.residue:
			if residue.name == name:
				self.residue.remove(residue)


	def read(self,file):

		"""
		reads an NMR specturm in its own format
		"""

		try:
			FILE = open(file)
		except:
			print "unable to open file"
			return

		previd = ""
		res = None
		for line in FILE.readlines():
			line = string.rstrip(line)

			id   = int(line[0:4])
			resn = line[5:8]
			atmn = line[12:16]
			cs   = float(line[17:25])

			if len(line) > 25:
				std  = float(line[26:34])
			else:
				std  = 0.0


			if id != previd:
				res    = self.newResidue()
				res.id = id
				res.name = resn

			atom = res.newAtom()
			atom.resi = id
			atom.name = atmn
			atom.cs_value = cs
			atom.cs_stdev = std

		FILE.close()


	def write(self, file):

		"""
		writes an NMR spectrum in its own format
		"""

		try:
			FILE = open(file, 'w')
		except:
			print "unable to open file"
			sys.exit()

		for res in self.residue:
			for atom in res.atom:
				FILE.write("%4i %3s    %4s %8.4f %8.4f\n" % (res.id, res.name, atom.name, atom.cs_value, atom.cs_stdev))

		FILE.close()
