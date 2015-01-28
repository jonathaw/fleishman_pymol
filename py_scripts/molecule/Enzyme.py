#!/usr/bin/python


"""

	Enzyme.py

	class for representing Enzymes
	They have a protein, ligands, and virtual atoms

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import string
from Molecule import *
from match_routines import *


class Enzyme(Molecule):

	def __init__(self, name=""):
		Molecule.__init__(self)
		self.name         = name
		self.ligand       = None
		self.protein      = None
		self.virtualAtoms = []
		self.catalytic    = []


	def clear(self):

		"""
		clears all arrays in the enzyme
		"""

		Molecule.clear(self)
		self.virtualAtoms = []
		self.catalytic    = []
		self.ligand       = None
		self.protein      = None


	def clone(self):

		"""
		creates a deep copy of the enzyme
		"""

		newenz = Enzyme()
		newenz = Molecule.clone(self,replica=newenz)
		return newenz


	def readPDB(self,file):

		"""
		reads a pdbfile and sets up the ligand and catalytic residues
		"""

		Molecule.readPDB(self,file)
		if len(self.chain) == 0:
			return

		chainA = self.getChain("A")
		if chainA == None:
			self.protein = self.chain[0]
			chainA = self.protein
		else:
			self.protein = chainA

		ligs = self.getHeteroAtoms()
		if len(ligs) > 0:
			LG1 = self.getResiduesByName("LG1")
			if len(LG1) == 0:
				self.ligand = ligs[0]
				if ligs[0] in self.protein.residue:
					self.protein.residue.remove(ligs[0])
			else:
				if LG1[0] in self.protein.residue:
					self.protein.residue.remove(LG1[0])
					newchain = self.newChain()
					newchain.addResidue(LG1[0])

				self.ligand = LG1[0]
				

			for lig in ligs:
				for atm in lig.atom:
					if atm.name[0] == "V":
						self.virtualAtoms.append(atm)



		# --- get catalytic residues --- #
		temp1 = re.compile("REMARK BACKBONE TEMPLATE")
		temp2 = re.compile("REMARK ROSETTA_MATCH TEMPLATE")
		temp3 = re.compile("REMARK   0 BONE TEMPLATE")
		ncat = 0
		for rem in self.remark:
			if temp1.search(rem):
				ncat += 1
			elif temp2.search(rem):
				ncat += 1
			elif temp3.search(rem):
			#	print "Newest fomart found"
				ncat += 1


		if ncat > 0:
			nline = 0
			self.catalytic = [None]*ncat
			for rem in self.remark:
				if temp1.search(rem):
					cols = rem.split()
					res  = cols[10]
					pos  = int(cols[11])-1
					cres = chainA.getResidue(res)
					if cres == None:
						print "cannot find catalytic residue:",res
						print "     file = ",file
						self.catalytic = []
						return
						#sys.exit()
					ires = int(nline)
					self.catalytic[pos] = cres
					cres.cat = pos
					nline += 1
				elif temp2.search(rem):
					cols = rem.split()
					res  = cols[9]
					res  = res[3:]
					cres = chainA.getResidue(res)
					if cres == None:
						print "cannot find catalytic residue:",res
					ires = int(nline)
					self.catalytic[nline] = cres
					cres.cat = nline
					nline += 1



	def isCatalytic(self, res=None, resid=-1):

		"""
		checks to see if the residue (or resid) is catalytic
		"""

		if res != None:
			for cres in self.catalytic:
				if res == cres:
					return True
		elif resid != -1:
			for cres in self.catalytic:
				if resid == int(cres.file_id):
					return True
		else:
			return False



	def numCatalytic(self):

		"""
		returns the number of catalytic residues
		"""

		return len(self.catalytic)
