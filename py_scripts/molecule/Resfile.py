#!/usr/bin/python


__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import string

class Resfile:

	"""
	class used to store and manipulate resfiles used by rosetta
	"""


	def __init__(self):
		self.native  = []
		self.type    = []
		self.allowed = []



	def clear(self):
	
		"""
		clears the class to be reused
		"""

		self.native  = []
		self.type    = []
		self.allowed = []



	def read(self, file):

		"""
		reads in a resfile
		"""

		try:
			FILE = open(file)	
		except:
			print "unable to open file"
			sys.exit()

		lines = FILE.readlines()

		for i in range(26,len(lines)):
			line = string.rstrip(lines[i])
			cols = line.split()
			self.native.append("G")
			self.type.append(cols[3])
			self.allowed.append("")
			if len(cols) == 5:
				iall = len(self.allowed) - 1
				self.allowed[iall] = cols[4]

		FILE.close()



	def write(self, file):

		"""
		writes a resfile
		"""

		try:
			FILE = open(file, 'w')
		except:
			print "unable to write file"
			return

		FILE.write("""This file specifies which residues will be varied

 Column   2:  Chain
 Column   4-7:  sequential residue number
 Column   9-12:  pdb residue number
 Column  14-18: id  (described below)
 Column  20-40: amino acids to be used

 NATAA  => use native amino acid
 ALLAA  => all amino acids
 NATRO  => native amino acid and rotamer
 PIKAA  => select inividual amino acids
 POLAR  => polar amino acids
 APOLA  => apolar amino acids

 The following demo lines are in the proper format

 A    1    3 NATAA
 A    2    4 ALLAA
 A    3    6 NATRO
 A    4    7 NATAA
 B    5    1 PIKAA  DFLM
 B    6    2 PIKAA  HIL
 B    7    3 POLAR""")
		FILE.write("\n -------------------------------------------------\n")
		FILE.write(" start\n")	

		for i in range(len(self.native)):
			FILE.write(" %5d A %5s   %s\n" % (i+1,self.type[i],self.allowed[i]))
	#		FILE.write(" A%5d%5d %5s   %s\n" % (i+1,i+1,self.type[i],self.allowed[i]))

		FILE.close()
		


	def numResidues(self):
	
		"""
		returns the number of residues in the resfile
		"""

		return len(self.native)



	def setMolecule(self, mol=None):
		
		"""
		sets the molecule to use for the resfile
		only the first chain is used
		"""

		if mol == None:
			return

		self.native = []
		self.type   = []
		for chn in mol.chain:
			for res in chn.residue:
				self.native.append(res.aa1())
				self.type.append("NATRO")
				self.allowed.append("")


	def addResidue(self, res="G"):

		self.native.append(res)
		self.type.append("NATRO")
		self.allowed.append(" ")



	def setType(self, index=-1, type=""):

		"""
		sets the type of a given residue
		"""

		if index >= 0 and index < self.numResidues():
			self.type[index] = type



	def repackOnly(self, index=-1):
		
		"""
		only allows the residue to be repacked
		"""

		self.setType(index, "NATAA")
		self.allowed[index] = ""



	def designOnly(self, index=-1):

		"""
		makes the residue fully designable
		"""

		self.setType(index, "ALLAA")


	def designResidue(self, index=-1, allowed=""):

		self.setType(index, "PIKAA")
		self.allowed[index] = allowed


	
	def designNoGly(self, index=-1):

		self.setType(index, "PIKAA")
		self.allowed[index] = "ACDEFHIKLMNPQRSTVWY"



	def polarOnly(self, index=-1):

		"""
		allows only polar residues to be designed at the position
		"""	
		
		self.setType(index, "POLAR")		
		

		
	def nonpolarOnly(self, index=-1):

		"""
		allows only nonpolar residues to be designed at the position
		"""

		self.setType(index, "APOLA")



	def fixedRotamer(self, index=-1):

		"""
		only make a residue fixed rotamer
		"""

		self.setType(index, "NATRO")
		self.allowed[index] = ""



	def setCatalytic(self, index=-1):

		"""
		residue is catalytic
		"""

		self.setType(index, "NATRO")



	def designedResidues(self):

		"""
		returns a list of designed residues
		"""

		des = []
		for i in range(len(self.type)):
			if self.type[i] == "ALLAA" or self.type[i] == "PIKAA":
				des.append(i+1)

		return des



	def repackedResidues(self):

		"""
		returns a list of repacked residues
		"""

		rep = []
		for i in range(len(self.type)):
			if self.type[i] == "NATAA":
				rep.append(i+1)

		return rep


	def restrictBy(self, index, restriction=""):

		"""
		restricts the current pikaa's by a given restriction
		"""

		for i in restriction:
			self.allowed[index] = self.allowed[index].replace(i,"")


	def expandBy(self, index, expansion=""):

		"""
		expands the current pikaa's by a given allowance
		"""

		for i in expansion:
			if not i in self.allowed[index]:
				self.allowed[index] += i

