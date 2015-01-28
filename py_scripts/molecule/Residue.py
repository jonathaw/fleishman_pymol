#!/usr/bin/python

"""

	Residue.py

	The residue class is a storage class for atoms

"""

__author__ = ['Andrew Wollacott amw215@u.washington.edu']
__version__ = "Revision 0.1"


from Atom import *



class Residue:

	"""
	The residue class is a storage class for atoms
	"""

	def __init__(self, name=""):
		self.name        = name
		self.file_id     = 0
		self.atom        = []
		self.parentChain = None
		self.terminal    = 0
		self.phi         = 0
		self.psi         = 0
		self.ome         = 0
		self.chi1        = 0
		self.chi2        = 0
		self.chi3        = 0
		self.chi4        = 0
		self.ss          = ""
		self.cat         = -1

		# rosetta energy terms
		self.Erep        = 0.0
		self.Eatr        = 0.0
		self.EhbSC       = 0.0
		self.EhbBB       = 0.0
		self.Egb         = 0.0
		self.Eres        = 0.0
		self.Ecst        = 0.0
		self.Esol        = 0.0
		self.Edun        = 0.0



	def __getitem__(self, key):

		"""
		returns an atom of a given index
		"""

		if key < 0 or key >= len(self.atom):	
			return None

		return self.atom[key]


	def __repr__(self):	
		
		"""
		prints the residue
		"""

		repr = ""
		natoms = self.numAtoms()
		for i in range(natoms):
			repr += self.atom[i].display()

			if i < natoms-1:
				repr += "\n"

		return repr
			


	def copy(self, rhs):

		"""
		function copy: does not return a deep copy of the residue
		"""

		self.name    = rhs.name
		self.file_id = rhs.file_id
		self.phi     = rhs.phi
		self.psi     = rhs.psi
		self.ome     = rhs.ome
		self.chi1    = rhs.chi1
		self.chi2    = rhs.chi2
		self.chi3    = rhs.chi3
		self.chi4    = rhs.chi4
		self.ss      = rhs.ss
		self.cat     = rhs.cat

		# rosetta energy terms
		self.Erep    = rhs.Erep
		self.Eatr    = rhs.Eatr
		self.EhbSC   = rhs.EhbSC
		self.EhbBB   = rhs.EhbBB
		self.Egb     = rhs.Egb
		self.Eres    = rhs.Eres
		self.Ecst    = rhs.Ecst
		self.Esol    = rhs.Esol
		self.Edun    = rhs.Edun

	

	def clone(self):

		"""
		function clone: creates a replica of the current residue
		"""

		replica = Residue()
		replica.copy(self)

		for atom in self.atom:
			newatom = atom.clone()
			replica.addAtom(newatom)

		return replica



	def clear(self):

		"""
		function clear: clears the atoms in the residue
		"""

		self.atom = []



	def numAtoms(self):

		"""
		function numAtoms: returns the number of atoms in the residue
		"""

		return len(self.atom)



	def atomExists(self, name):

		"""
		function atomExists: checks whether an atom of a given name exists
		"""

		for i in self.atom:
			if i.name == name:
				return True

		return False



	def getAtom(self, name):

		"""
		function getAtom: returns the atom of a given name
		"""

		for atom in self.atom:
			if atom.name == name:
				return atom

		return None



	def getAtomIndex(self, name):
		
		"""
		function getAtomIndex: returns the index of the atom of a given name
		"""

		for i in range(len(self.atom)):
			if self.atom[i].name == name:
				return i

		return -1



	def addAtom(self, myatom):
		
		"""
		function addAtom: adds an atom to the current residue
		"""

		self.atom.append(myatom)
		myatom.parentResidue = self

		# --- WARNING
		# --- the following values may become old and outdated
		myatom.resn = self.name
		myatom.resi = self.file_id



	def newAtom(self):

		"""
		function newAtom: creates and returns an atom in the current residue
		"""

		myatom = Atom()
		self.addAtom(myatom)
		return myatom



	def mass(self):

		"""
		function mass: returns the mass of the residue
		"""

		itsMass = 0
		for atom in self.atom:
			itsMass += atom.mass

		return itsMass
			


	def charge(self):

		"""
		function charge: returns the charge of the residue
		"""

		itsCharge = 0
		for atom in self.atom:
			itsCharge += atom.charge

		return itsCharge



	def translate(self, vec):

		"""
		function translate: translates a residue by a given vector
		"""

		for atom in self.atom:
			atom.translate(vec)



	def removeAtom(self, name):

		"""
		removes an atom with given name
		"""
		
		atm = self.getAtom(name)
		if atm == None:
			print "cannot remove atom",name
			return

		self.atom.remove(atm)



	def keepOnlyTheseAtoms(self, namelist=None):

		"""
		keeps only atoms with the specified names
		"""

		remlist = []
		for atm in self.atom:
			if not atm.name in namelist:
				remlist.append(atm)

		for atm in remlist:
			self.atom.remove(atm)



	def removeAtomsContaining(self, name):
	
		"""
		removes atoms with names containing a given string
		"""

		remlist = []
		for atm in self.atom:
			if name in atm.name:
				remlist.append(atm)
				
		for atm in remlist:
			self.atom.remove(atm)



	def com(self):

		"""
		returns the center of mass of the residue
		"""

		mycom = vector3d()
		nat = 0.0
		for atm in self.atom:
			mycom.x += atm.coord.x
			mycom.y += atm.coord.y
			mycom.z += atm.coord.z

			nat += 1.0

		if nat == 0:
			print "ERROR: zero atoms for COM calculation!"
			sys.exit()

		mycom /= nat
		return mycom



	def aa1(self):

		"""
		function aa1: returns the 1 letter code of the residue name
		"""

		if self.name == "ALA": return "A"
		if self.name == "CYS": return "C"
		if self.name == "CYX": return "C"
		if self.name == "ASP": return "D"
		if self.name == "GLU": return "E"
		if self.name == "PHE": return "F"
		if self.name == "GLY": return "G"
		if self.name == "HIS": return "H"
		if self.name == "HID": return "H"
		if self.name == "HIE": return "H"
		if self.name == "ILE": return "I"
		if self.name == "LYS": return "K"
		if self.name == "LEU": return "L"
		if self.name == "MET": return "M"
		if self.name == "ASN": return "N"
		if self.name == "PRO": return "P"
		if self.name == "GLN": return "Q"
		if self.name == "ARG": return "R"
		if self.name == "SER": return "S"
		if self.name == "THR": return "T"
		if self.name == "VAL": return "V"
		if self.name == "TRP": return "W"
		if self.name == "TYR": return "Y"
		return "x" 

