#!/usr/bin/python

"""

	ligand.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


from Residue import *
from ligand_atom import *

class ligand(Residue):

	"""
	The ligand class is derived from the residue class
	"""

	def __init__(self):
		Residue.__init__(self)
		self.ring = []
		self.rotatable = []	
		self.index = 0
		


	def newAtom(self):

		"""
		function newAtom: creates a new ligand_atom
		"""

		myatom = ligand_atom()
		self.addAtom(myatom)
		return myatom


	def readPDB(self, file):
		pass


	def writePDB(self, file):
		pass



	def setTree(self, name="", type=""):
		id = self.getAtomIndex(name)
		if id < 0:
			print "cannot find atom",name
			return

		print "making ",name,type
		self.atom[id].tree = type



	def setRotatableBond(self, atom1=None, atom2=None):
		if isinstance(atom1, str):
			id1 = self.getAtomIndex(atom1)
			if id1 < 0:
				print "ligand: cannot find atom:", atom1

			id2 = self.getAtomIndex(atom2)
			if id2 < 0:
				print "ligand: cannot find atom:", atom1

		
		bnd = []
		atm1 = self.atom[id1].index
		atm2 = self.atom[id2].index
		bnd.append(atm1)
		bnd.append(atm2)
		self.rotatable.append(bnd)


	def removeRotatableBond(self, atom1=None, atom2=None):
		id1 = self.getAtomIndex(atom1)
		id2 = self.getAtomIndex(atom2)

		for bond in self.rotatable:
			if bond[0] == id1 and bond[1] == id2:
				self.rotatable.remove(bond)
				return
			if bond[0] == id2 and bond[1] == id1:
				self.rotatable.remove(bond)
				return

	
	def isBondRotatable(self, atom1=None, atom2=None):
		id1 = self.getAtom(atom1).index
		id2 = self.getAtom(atom2).index

		for bond in self.rotatable:
			if bond[0] == id1 and bond[1] == id2:
				return True
			if bond[0] == id2 and bond[1] == id1:
				return True

		return False


	def isAtomRotatable(self, atom1=None):
		id1 = self.getAtom(atom1).index

		for bond in self.rotatable:
			if bond[0] == id1 or bond[1] == id1:
				return True

		return False



	def perceiveBonds(self):
		for i in range(len(self.atom)):
			print "bonding",self.atom[i].name
			for j in range(len(self.atom)):
				if i == j:
					continue

				dist = self.atom[i].distance(self.atom[j])
				if dist < 1.95:
					self.atom[i].bonds.append(j)
					print "   ",self.atom[j].name
			#print self.atom[i].name,len(self.atom[i].bonds)


	def getMainAtoms(self):
		atmlist = []
		for atm in self.atom:
			if atm.tree == "M":
				id = self.getAtomIndex(atm.name)
				if id >= 0:
					atmlist.append(id)
				
		return atmlist


	def getNonMainAtoms(self):
		atmlist = []
		for atm in self.atom:
			if atm.tree != "M":
				id = self.getAtomIndex(atm.name)
				if id >= 0:
					atmlist.append(id)
				
		return atmlist


	def buildTree(self):
		self.perceiveBonds()
		mainlist = self.getMainAtoms()
		self.buildMain()		
		self.buildNonMain()

					
		
	def buildMain(self):
		mainlist = self.getMainAtoms()

		# ---   get the ends of the main chain   --- #
		ends = []
		for id1 in mainlist:
			atm1 = self.atom[id1]
			nbnd = 0
			for j in range(len(atm1.bonds)):
				id2 = atm1.bonds[j]
				atm2 = self.atom[id2]
				if atm2.tree == "M":
					nbnd += 1
					if nbnd > 2:
						print "too many main atoms bound to each other"

					print atm1.name,atm2.name
			if nbnd == 1:
				ends.append(id1)


		if len(ends) != 2:
			print "number of ends = ",len(ends)
			print "ERROR DETERMINING MAIN12"
			return


		# ---   build up from the ends   --- #
		id1 = ends[0]
		atm1 = self.atom[id1]
		self.atom[id1].bnd12 = -1
		self.atom[id1].bnd13 = -2
		self.atom[id1].bnd14 = -3
		for i in range(len(mainlist)):
			self.index += 1
			self.atom[id1].index = self.index
			atm1 = self.atom[id1]
			#print "atom1 = ",atm1.name,"index=",atm1.index,"bnd12 = ",atm1.bnd12
			for j in range(len(atm1.bonds)):
				id2 = atm1.bonds[j]

				if self.atom[id2].tree == "M":
					#print "checking ",self.atom[id2].name,self.atom[id2].bnd12
					if self.atom[id2].index == self.atom[id1].bnd12:
						continue

					#print "   ",self.atom[id2].name
					self.atom[id2].bnd12 = self.atom[id1].index
					self.atom[id2].bnd13 = self.atom[id1].bnd12
					self.atom[id2].bnd14 = self.atom[id1].bnd13
					kept = id2

			id1 = kept

			


	def buildNonMain(self):	
		mainlist = self.getMainAtoms()

		for id1 in mainlist:
			self.recursiveBuilder(id1)


	def recursiveBuilder(self, id1):
		atm1 = self.atom[id1]
		for id in atm1.bonds:
			if atm1.bnd12 == self.atom[id].index:
				continue

			if self.atom[id].tree == "M":
				if self.atom[id].bnd12 != self.atom[id1].index:
					self.addRing(self.atom[id].index, self.atom[id1].index)
				continue


			if self.atom[id].index == -9:
				self.index += 1
				self.atom[id].index = self.index
				self.atom[id].bnd12 = atm1.index
				self.atom[id].bnd13 = atm1.bnd12
				self.atom[id].bnd14 = atm1.bnd13
				if len(self.atom[id].bonds) == 1:
					self.atom[id].tree = "T"
				else:
					self.atom[id].tree = "B"

			self.recursiveBuilder(id)

		return

		
	def addRing(self,id1,id2):
		bnd = [id1,id2]
		if not self.isRingPresent(id1,id2):
			self.ring.append(bnd)


	def isRingPresent(self,id1,id2):
		for ring in self.ring:
			if ring[0] == id1 and ring[1] == id2:
				return True
			if ring[0] == id2 and ring[1] == id1:
				return True

		return False

