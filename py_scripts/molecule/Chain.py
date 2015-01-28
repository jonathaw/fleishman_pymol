#!/usr/bin/python


"""
	
	Chain.py

	A chain contains a list of residues

"""


__author__ = ['Andrew Wollacott  amw215@u.washington.edu']
__version__ = "Revision 0.1"


from Residue import *
import sys


class Chain:

	"""
	The chain class is a storage class for residues
	"""

	def __init__(self, name=""):

		self.name           = name
		self.residue        = []	
		self.parentMolecule = None



	def __getitem__(self, key):

		"""
		returns a residue of given index
		"""

		if key < 0 or key >= len(self.residue):
			return None

		return self.residue[key]



	def copy(self, rhs):

		"""
		function copy: does not provide a deep copy of the chain
		"""

		self.name = rhs.name



	def clone(self):

		"""
		function clone: provides a deep copy replica of the chain
		"""

		replica = Chain()
		replica.copy(self)

		for res in self.residue:
			newres = res.clone()
			replica.addResidue(newres)

		return replica



	def clear(self):

		"""
		function clear: clears the residue array
		"""

		for residue in self.residue:
			residue.clear()

		self.residue = []



	def addResidue(self, res):

		"""
		function addResidue: adds a residue to the chain
		"""

		self.residue.append(res)
		res.parentChain = self



	def addResidueList(self, reslist):

		"""
		function addResidueList: adds a list of residues to the chain
		"""

		for res in reslist:
			self.residue.append(res)
			res.parentChain = self



	def getResidue(self, resi):

		"""
		function getResidue: returns the residue of a given file_id
		"""

		for res in self.residue:
			if int(res.file_id) == int(resi):
				return res

		return None



	def getResidues(self, beg, end):
		
		"""
		returns a list of residues using their file_id between beg and end (inclusive)
		"""

		reslist = []
		if end < beg:
			print "chain:getResidues: end index must be greater than beginning index"
			return reslist

		for res in self.residue:
			if int(res.file_id) >= beg and int(res.file_id) <= end:
				reslist.append(res)

		return reslist



	def getResiduesByName(self, resn):

		"""
		returns a list of residues with matching names
		"""

		reslist = []
		for res in self.residue:
			if res.name == resn:
				reslist.append(res)

		return reslist
					


	def residueExists(self, res):

		"""
		function residueExists: checks whether a residue of given file_id exists
		"""

		for i in self.residue:
			if i.file_id == res:
				return True

		return False



	def getResidueIndex(self, resi):

		"""
		function getResidueIndex: returns the residue index of a given file_id
		"""

		for i in range(len(self.residue)):
			if int(self.residue[i].file_id) == int(resi):
				return i
		
		return None
		


	def newResidue(self):

		"""
		function newResidue: creates and returns a new residue in the chain
		"""

		myres = Residue()
		self.addResidue(myres)
		return myres



	def replaceResidue(self, resi, newres):
		
		"""
		replaces a residue of given file_id with another residue
		"""

		index = self.getResidueIndex(resi)
		if index == None:
			print "cannot find residue of index:",resi
			sys.exit()

		curr_res = self.getResidue(resi)	
		self.residue[index] = newres
		newres.file_id = str(resi)



	def insertResidue(self, res, resi):

		"""
		inserts a residue at a given point
		"""
		
		i = self.getResidueIndex(resi)

		if i == None:
			print "cannot find residue for insertion:",resi
			return

		self.residue.insert(i+1, res)



	def insertResidues(self, list, beg):

		"""
		function insertResidues: inserts a list of residues at a given point
		"""

		i = self.getResidueIndex(beg)
		if i == None:
			print "cannot find residue:",beg
			return

		i += 1

		for j in range(len(list)):
			self.residue.insert(i+j, list[j])



	def numResidues(self):

		"""
		function numResidues: returns the number of residues in the chain
		"""

		return len(self.residue)



	def numResn(self, name):
	
		"""
		returns the number of residues of a given name
		"""

		nres = 0
		for res in self.residue:
			if res.name == name:
				nres += 1

		return nres



	def numAtoms(self):

		"""
		function numAtoms: returns the number of atoms in a chain
		"""

		natom = 0
		for i in self.residue:
			natom += i.numAtoms()

		return natom



	def translate(self, vec):
		
		"""
		function translate: translates a chain by a given vector
		"""

		for res in self.residue:
			res.translate(vec)
			

	
	def slice(self, beg, end):
		
		"""
		function slice: removes a slice of residues using their file_ids
		"""

		for i in range(beg,end+1):
			myres = self.getResidue(i)
			if myres == None:
				print "cannot slice residue",i
				continue

			self.residue.remove(myres)	


	def removeResidue(self,resi):

		"""
		function removeResidue: removes a residue from the chain using its file_id
		"""

		myres = self.getResidue(resi)
		if myres == None:
			print "cannot remove residue",resi
			return

		self.residue.remove(myres)



	def renumber(self,resRenumber=True,atomRenumber=True):
		
		"""
		renumbers residues an/or atoms in a chain
		"""
	
		nres = 0
		natm = 0
		for res in self.residue:
			nres += 1
			if resRenumber:
				res.file_id = nres

			for atm in res.atom:
				natm += 1
				if atomRenumber:
					atm.file_id = natm



	def atomList(self):

		"""
		returns a list of atoms in the chain
		"""

		al = []
		for res in self.residue:
			for atm in res.atom:
				al.append(atm)

		return al
							
	

	def sequence(self):

		"""
		returns the residue sequence of the chain
		"""

		seq = ""
		for res in self.residue:
			seq += res.aa1()	

		return seq


	
	def com(self):

		"""
		returns the center of mass of the chain
		"""

		mycom = vector3d()
		nat = 0.0
		for res in self.residue:
			for atm in res.atom:
				mycom += atm.coord
				nat += 1.0

		mycom /= nat
		return mycom

	
