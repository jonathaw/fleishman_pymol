#!/usr/bin/python


"""

	Molecule.py

	class for representing molecules

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import string,sys
import re
from Chain import *
from PeriodicTable import *

_molelement = {}
_molelement["aroC"] = "C"
_molelement["Nhis"] = "N"
_molelement["OCbb"] = "O"
_molelement["COO "] = "C"
_molelement["OOC "] = "O"
_molelement["Haro"] = "H"
_molelement["Hapo"] = "H"
_molelement["CH3 "] = "C"
_molelement["CH1 "] = "C"
_molelement["CH2 "] = "C"
_molelement["Npro"] = "N"
_molelement["CNH2"] = "C"
_molelement["OH  "] = "O"
_molelement["NH2O"] = "N"
_molelement["ONH2"] = "O"
_molelement["Hpol"] = "H"
_molelement["HOH "] = "O"


class Molecule:

	"""
	The molecule class is a storage class for chains
	"""

	def __init__(self, name=""):
		self.name  = name
		self.chain = []
		self.file  = ""
		self.periodic = PeriodicTable()
		self.remark = []
		self.bk_tot = 0.0
		self.fa_rep = 0.0
		self.fa_atr = 0.0



	def copy(self, rhs):

		"""
		does not perform a deep copy of the molecule
		"""

		self.name = rhs.name
		self.file = rhs.file

		for rem in rhs.remark:
			self.addRemark(rem)

		self.bk_tot = rhs.bk_tot
		self.fa_rep = rhs.fa_rep
		self.fa_atr = rhs.fa_atr



	def clone(self, replica=None):

		"""
		creates and returns a deep copy of the molecule
		"""

		if replica == None:
			replica = Molecule()

		replica.copy(self)

		for chain in self.chain:
			newchain = chain.clone()
			replica.addChain(newchain)

		return replica



	def clear(self):

		"""
		clears the arrays stored in the molecule
		"""

		for chain in self.chain:
			chain.clear()

		self.chain = []
		self.remark = []



	def getChain(self, chain):

		"""
		returns a chain of given name
		"""

		for i in self.chain:
			if i.name == chain:
				return i

		return None



	def chainExists(self, chain):

		"""
		checks whether a chain of given name exists in the molecule
		"""

		for i in self.chain:
			if i.name == chain:
				return True

		return False



	def addChain(self, chain):

		"""
		adds a chain to the molecule
		"""

		self.chain.append(chain)
		chain.parentMolecule = self



	def newChain(self):

		"""
		creates and returns a new chain
		"""

		mychain = Chain()
		self.addChain(mychain)
		return mychain



	def numChains(self):

		"""
		returns the number of chains in the molecule
		"""

		return len(self.chain)



	def numResidues(self):

		"""
		returns the number of residues across all chains
		"""

		nres = 0
		for chain in self.chain:
			nres += chain.numResidues()

		return nres



	def numAtoms(self):
		
		"""
		returns the number of atoms in the molecule
		"""

		natoms = 0
		for chain in self.chain:
			for residue in chain.residue:
				natoms += residue.numAtoms()

		return natoms



	def sequence(self):

		"""
		returns the sequence of the molecule
		"""

		seq = ""
		for chain in self.chain:
			for res in chain.residue:
				seq += res.aa1()

		return seq



	def addRemark(self, rem):

		"""
		adds a remark that is printed out in output files
		"""

		self.remark.append(rem)


	def renumber(self):

		"""
		renumbers the molecule
		"""
		
		ires = 1
		iatm = 1
		for mychain in self.chain:
			for myres in mychain.residue:
				myres.file_id = ires
				ires += 1
				for myatm in myres.atom:
					myatm.file_id = iatm
					iatm += 1
					
				




	def writePDB(self, file, resRenumber=True, atomRenumber=True, start_res=1):

		"""
		writes the molecule in pdb format
		"""

		try:
			PDB = open(file, 'w')
		except:
			print "cannot open file"
			return 0

		for remark in self.remark:
			PDB.write(remark + "\n")

		nres = start_res - 1
		natoms = 0
		for chain in self.chain:
			for residue in chain.residue:

				if residue.numAtoms() > 0:
					nres += 1
				
				if not resRenumber:
					nres = int(residue.file_id)

				for atom in residue.atom:
					natoms += 1
					natoms = min(9999,natoms)


					if not atomRenumber:
						natoms = int(atom.file_id)

					PDB.write('%6s%5i %4s %3s %1s%4i   %1s%8.3f%8.3f%8.3f%6.2f%6.2f%s\n' %
						(atom.kind, natoms, atom.name, residue.name, chain.name, nres, atom.local,
						atom.coord.x, atom.coord.y, atom.coord.z, atom.occupancy,
						atom.bfactor,atom.rest))

			PDB.write("TER\n")
		PDB.write("END\n")
					
				
		PDB.close()



	def readPDB(self, file):

		"""
		reads in a molecule in pdb format
		"""

		try:
			pdb = open(file, 'r')
		except:
			print "cannot open pdbfile",file
			return 0

		self.file = file
		presi = ""
		presn = ""
		prevc = ""
		nlines = 0
		mychain = None
		myres = Residue()
		term = 1
		rescore = re.compile("res aa    Eatr")
		re_bk_tot = re.compile("bk_tot")
		re_fa_rep = re.compile("fa_rep")
		re_fa_atr = re.compile("fa_atr")
		bReadScore = False
		for line in pdb.readlines():
			line = string.strip(line)

			if line[0:3] == "REM":
				self.addRemark(line)

			if line[0:3] == "TER":
				term = 1

			if rescore.search(line):
				bReadScore = True
				continue

			# read rosetta residue-based scoring information
			if bReadScore:
				cols = line.split()
				if cols[0] == "totals":
					bReadScore = False
					continue

				myres = self.getResidue(int(cols[0]))
				if myres == None:
					print "warning reading score!!! cannot find residue:",cols[0]

				myres.Eatr = float(cols[2])
				myres.Erep = float(cols[3])
				myres.Esol = float(cols[4])
				myres.Edun = float(cols[7])
				myres.EhbBB = float(cols[9])
				myres.EhbSC = float(cols[10])
				myres.Egb = float(cols[13])
				myres.Ecst = float(cols[16])
				myres.Eres = float(cols[17])
				
			# read atomic information
			if line[0:4] == "ATOM" or line[0:6] == "HETATM":
				chain = line[21:22]
				if chain != prevc or nlines == 0 or term:
					mychain = Chain()
					mychain.name = chain
					prevc = chain
					self.addChain(mychain)
				
				resi = line[22:26]
				resn = line[17:20]

				if nlines == 0 or presi != resi or presn != resn:
					if term:
						if myres:
							myres.terminal = "CTER"
						
					presi = resi
					presn = resn
					myres = Residue()
					myres.name = line[17:20]
					myres.file_id = resi
					mychain.addResidue(myres)

					if term:
						myres.terminal = "NTER"
						term = 0

				myatom = Atom()
				
				if line[0:4] == "HETA":
					myatom.kind = "HETATM"
				else:
					myatom.kind = "ATOM  "

				myatom.name      = line[12:16]
				myatom.file_id   = line[6:11]
				myatom.local     = line[29:30]
				myatom.coord[0] = float(line[30:38])
				myatom.coord[1] = float(line[38:46])
				myatom.coord[2] = float(line[46:54])
				
				
				if len(line) >= 66:
					tmpstr = line[54:68]
					tmplst = tmpstr.split()
					myatom.occupancy = float(tmplst[0])
					myatom.bfactor  = float(tmplst[1])
					#myatom.occupancy = float(line[54:60])
					#myatom.bfactor   = float(line[60:66])
					myatom.rest      = line[66:len(line)]

				self.__determineElement(myatom)
				myres.addAtom(myatom)
				
				nlines += 1

	########	if re_bk_tot.search(line):
	########		cols = line.split()
	########		self.bk_tot = float(cols[1])

	########	if re_fa_rep.search(line):
	########		cols = line.split()
	########		self.fa_rep = float(cols[1])

	########	if re_fa_atr.search(line):
	########		cols = line.split()
	########		self.fa_atr = float(cols[1])

		pdb.close()



	def readRosetta(self, file):

		"""
		reads in a molecule in rosetta output format
		"""

		self.readPDB(file)

		try:
			pdb = open(file, 'r')	
		except:
			print "unable to open file"
			return

		bReadBack = 0
		bReadChi  = 0
		chain = self.chain[0]
		for line in pdb.readlines():
			line = string.rstrip(line)

			if line[0:8] == "complete":
				bReadBack = 1
				bReadChi  = 0
				continue

			if line[0:14] == "absolute decoy":
				bReadChi = 1
				continue

			if bReadChi:
				if line[0:3] == "res":
					continue 

				index = int(line[0:4])	
				myres = chain.getResidue(index)

				myres.chi1 = float(line[10:19])
				myres.chi2 = float(line[20:29])
				myres.chi3 = float(line[30:39])
				myres.chi4 = float(line[40:49])

			if bReadBack:
				index = int(line[0:4])
				myres = chain.getResidue(index)

				myres.ss  = line[5:6]
				myres.phi = float(line[8:17])	
				myres.psi = float(line[17:26])
				myres.ome = float(line[26:35])
				


	def __determineElement(self, atom):

		"""
		determins the element form the atom name
		"""

		c1 = atom.name[0:1]
		c2 = atom.name[1:2]

		# virtual atoms
		if c1 == "V":
			atom.element = "V"
			atom.radius  = 0.0
			return

		for element in self.periodic.element_name:
			if c2 == element:
				atom.element = c2
				atom.radius  = self.periodic.element_radius[c2]
				return

		for element in self.periodic.element_name:
			if c1 == element:
				atom.element = c1
				atom.radius  = self.periodic.element_radius[c1]
				return

		if atom.name in _molelement.keys():
			atom.element = _molelement[atom.name]
			atom.radius = self.periodic.element_radius[atom.element]


	
	def translate(self, vec):

		"""
		translates the molecule by a given vector
		"""

		for chain in self.chain:
			chain.translate(vec)



	def com(self):

		"""
		returns the center of mass of the protein
		"""

		com = vector3d()

		com.x = 0.0; com.y = 0.0; com.z = 0.0
		nAt = 0.0

		for chain in self.chain:
			for residue in chain.residue:
				for atom in residue.atom:
					com.x += atom.coord.x
					com.y += atom.coord.y
					com.z += atom.coord.z

					nAt += 1.0

		if nAt == 0:
			print "ERROR: zero atoms present for COM calculation!"
			sys.exit()

		com /= nAt
		return com



	def atomList(self):

		"""
		creates and returns an array of the atoms in the molecule
		"""

		al = []	
		for chain in self.chain:
			for res in chain.residue:
				for atom in res.atom:
					al.append(atom)

		return al



	def residueList(self):
		
		"""
		creates and returns an array of the residues in the molecule
		"""

		rl = []
		for chain in self.chain:
			for res in chain.residue:
				rl.append(res)

		return rl



	def getResidue(self, resi):
		
		"""
		returns the residue of given index (first found)
		"""

		if self.numChains == 0:
			print "WARNING: Molecule has no chains"
			return None

		resi = int(resi)
		for chn in self.chain:
			for res in chn.residue:
				if int(res.file_id) == resi:
					return res

		return None



	def getResiduesByName(self, resn):

		"""
		returns a list of residues with a given name
		"""

		reslist = []
		for chn in self.chain:
			for res in chn.residue:
				if res.name == resn:
					reslist.append(res)

		return reslist



	def getHeteroAtoms(self):

		"""
		returns a list of residues containing hetero atoms
		"""

		hetlist = []
		for chain in self.chain:
			for res in chain.residue:
				for atm in res.atom:
					if atm.kind == "HETATM":
						hetlist.append(res)		
						break

		return hetlist



	def getAtom(self, atomid):
	
		"""
		returns the first atom that matches the file id
		"""

		for chain in self.chain:
			for res in chain.residue:
				for atm in res.atom:
					if atomid == int(atm.file_id):
						return atm

		return None



	def removeChain(self, mychain):
		
		"""
		removes a chain of given name
		"""

		ichain = self.getChain(mychain)	
		if ichain == None:
			return

		self.chain.remove(ichain)

