#!/usr/bin/python


"""

	Selection.py

	class for defining molecular selections

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string
from Enzyme import *
from mol_routines import *


class Selection:

	def __init__(self):
		self.atomid   = []
		self.resi     = []
		self.resn     = []
		self.atom     = []
		self.element  = []
		self.chain    = []
		self.type     = []
		self.inverted = False
		self.atomlist = []
		self.keeplist = []
		self.macros   = []
		self.cat      = []

		self.invresi    = False
		self.invresn    = False
		self.invatom    = False
		self.invelement = False
		self.invchain   = False
		self.invtype    = False
		self.invatomid  = False
		self.invcat     = False


	
	def clear(self):

		"""
		clears all defined selections
		"""

		self.atomid   = []
		self.resi     = []
		self.resn     = []
		self.atom     = []
		self.element  = []
		self.chain    = []
		self.type     = []
		self.inverted = False
		self.atomlist = []
		self.keeplist = []
		self.macros   = []

		self.invresi    = False
		self.invresn    = False
		self.invatom    = False
		self.invelement = False
		self.invchain   = False
		self.invtype    = False
		self.invatomid  = False


	def parseMacros(self, selection=""):

		"""
		example:
		{around 5.0 [atomid=9001-9015]};type=ATOM  
		"""

		while True:
			start_index = selection.find("{")
			if start_index == -1:
				break

			end_index = selection.rfind("}")

			mystring = selection[start_index+1:end_index]

			si = mystring.find("[")
			ei = mystring.rfind("]")

			cols = mystring.split()
			mymacro = macro_selection()
			mymacro.type = cols[0]
			if mymacro.type == "around" or mymacro.type == "expand":
				mymacro.cutoff = float(cols[1])
			else:
				print "unrecognized macro!:",mymacro.type
				sys.exit()
				

			mymacro.selection.makeSelection(mystring[si+1:ei])
			self.macros.append(mymacro)

			selection = selection[end_index+1:]

		return selection
			


	def makeSelection(self, selection=""):

		"""
		parses and updates the internal selection criteria
		"""

		if selection == "":
			print "usage: makeSelection(selection)"

		sel_string = self.parseMacros(selection)

		# ---   split by ";"   --- #
		tmp = []
		cols = []
		cols = sel_string.split(";")
		for col in cols:
			inverse = False
			if col == "":
				continue

			tmp = string.split(col, "=")
			if "!" in tmp[0]:
				inverse = True

			if "resi" in tmp[0]:
				self.parseResI(tmp[1])
				self.invresi = inverse
			elif "resn" in tmp[0]:
				self.parseResN(tmp[1])
				self.invresn = inverse
			elif "name" in tmp[0]:
				self.parseAtom(tmp[1])
				self.invatom = inverse
			elif "element" in tmp[0]:
				self.parseElement(tmp[1])
				self.invelement = inverse	
			elif "chain" in tmp[0]:
				self.parseChain(tmp[1])
				self.invchain = inverse
			elif "type" in tmp[0]:
				self.parseType(tmp[1])
				self.invtype = inverse
			elif "cat" in tmp[0]:
				self.parseCat(tmp[1])
				self.invcat = inverse
			elif "atomid" in tmp[0]:
				self.parseAtomid(tmp[1])
				self.invatomid = inverse
			elif "BB" in tmp[0]:
				self.parseAtom(" N  , CA , C  , O  ")
				self.invatom = False
			elif "CEN" in tmp[0]:
				self.parseAtom(" N  , CA , C  , O  , CB ")
				self.invatom = False
			elif "SC" in tmp[0]:
				self.parseAtom(" N  , CA , C  , O  ")
				self.invatom = True
			elif "HET" in tmp[0]:
				self.parseType("HETATM")
				self.invtype = inverse
			else:
				print "unrecognized selector: ",tmp[0]
				sys.exit()



	def parseResI(self, line):

		"""
		setup parsing by residue file id
		"""

		cols = string.split(line, ",")

		for col in cols:
			if "-" in col:
				(beg, end) = string.split(col, "-")
				beg = int(beg)
				end = int(end)
				for i in range(beg,end+1):
					self.resi.append(i)
			else:
				self.resi.append(int(col))


	def parseCat(self, line):
		
		"""
		parses catalytic residues
		"""

		cols = string.split(line, ",")
		for col in cols:
			if "-" in col:
				(beg,end) = string.split(col, "-")
				beg = int(beg)
				end = int(end)
				for i in range(beg,end+1):
					self.cat.append(i-1)
			else:
				self.cat.append(int(col)-1)



	def parseAtomid(self, line):

		"""
		setup parsing by atom id
		"""

		cols = string.split(line, ",")

		for col in cols:
			if "-" in col:
				(beg, end) = string.split(col, "-")
				beg = int(beg)
				end = int(end)
				for i in range(beg,end+1):
					self.atomid.append(i)
			else:
				self.atomid.append(col)

	

	def parseResN(self, line):
		
		"""
		setup parsing by residue name
		"""

		cols = string.split(line, ",")

		for col in cols:
			self.resn.append(col)
				


	def parseAtom(self, line):

		"""
		setup parsing by atom name
		"""

		cols = string.split(line, ",")

		for col in cols:
			self.atom.append(col)



	def parseElement(self, line):

		"""
		setup parsing by element type
		"""

		cols = string.split(line, ",")

		for col in cols:
			self.element.append(col)



	def parseChain(self, line):

		"""
		setup parsing by chain type
		"""

		cols = string.split(line, ",")

		for col in cols:
			self.chain.append(col)



	def parseType(self, line):

		"""
		setup parsing by type (HETATM vs ATOM)
		"""

		cols = string.split(line, ",")

		for col in cols:
			self.type.append(col)

	
		
	def apply_selection(self, mol=None, atmlist=None,return_mol=True):
		
		"""
		applies the selection to a given molecule returning a molecule meeting
		the selected criteria
		"""

		# extract atom list
		for macro in self.macros:
			if mol != None:
				atmlist = macro.apply_selection(atmlist=mol.atomList())
			elif atmlist != None:
				atmlist = macro.apply_selection(atmlist=atmlist)

		if atmlist == None:
			self.extractAtoms(mol)
		else:
			self.atomlist = []
			for atm in atmlist:
				self.atomlist.append(atm)

		self.selectChain()
		self.selectCat()
		self.selectResI()
		self.selectResN()
		self.selectName()
		self.selectElement()
		self.selectAtomid()
		self.selectType()

		if return_mol:
			newmol = self.assembleMol()
			return newmol
		else:
			return self.atomlist



	def extractAtoms(self, mol):
		
		"""
		internal function used to extract a list of atoms from the molecule
		"""

		self.atomlist = []
		for chain in mol.chain:
			for res in chain.residue:
				for atom in res.atom:
					self.atomlist.append(atom)



	def selectChain(self, inverse=False):

		"""
		select atoms that are part of a given chain
		"""

		# keep all atoms if chain not selected
		if len(self.chain) == 0:
			return
				
		tmplist = []	
		for atom in self.atomlist:
			found = False
			for chain in self.chain:
				if atom.parentResidue.parentChain.name == chain:
					found = True

			if found and not inverse:
				tmplist.append(atom)
			if not found and inverse:
				tmplist.append(atom)

		self.atomlist = tmplist

	

	def selectResI(self):

		"""
		select atoms that are part of a residue of given index
		"""

		if len(self.resi) == 0:	
			return

		tmplist = []
		for atom in self.atomlist:
			found = False
			for resi in self.resi:
				if int(atom.parentResidue.file_id) == resi:
					found = True
					break

			if found and not self.invresi:
				tmplist.append(atom)
			if not found and self.invresi:
				tmplist.append(atom)

		self.atomlist = tmplist



	def selectCat(self):

		"""
		selects atoms that are in a catalytic residue
		"""

		if len(self.cat) == 0:
			return

		tmplist = []
		for atom in self.atomlist:
			found = False

			for cat in self.cat:
				if atom.parentResidue.cat == cat:
					found = True
					break

			if found and not self.invcat:
				tmplist.append(atom)
			if not found and self.invcat:
				tmplist.append(atom)

		self.atomlist = tmplist
					


	
	def selectAtomid(self):

		"""
		select atoms in the molecule that have a given index
		"""

		if len(self.atomid) == 0:
			return

		tmplist = []
		for atom in self.atomlist:
			found = False
			for id in self.atomid:
				if int(id) == int(atom.file_id):
					found = True
					break


			if found and not self.invatomid:
				tmplist.append(atom)
			if not found and self.invatomid:
				tmplist.append(atom)

		self.atomlist = tmplist



	def selectResN(self):

		"""
		select atoms in the molecule that are part of a residue with a given name
		"""

		if len(self.resn) == 0:
			return

		tmplist = []
		for atom in self.atomlist:
			found = False
			for resn in self.resn:
				if atom.parentResidue.name == resn:
					found = True
					break

			if found and not self.invresn:
				tmplist.append(atom)
			if not found and self.invresn:
				tmplist.append(atom)

		self.atomlist = tmplist



	def selectName(self, inverse=False):
		
		"""
		select atoms that have a given name
		"""

		if len(self.atom) == 0:
			return

		tmplist = []
		for atom in self.atomlist:
			found = False
			for name in self.atom:
				if atom.name == name:
					found = True
					break

			if found and not self.invatom:
				tmplist.append(atom)
			if not found and self.invatom:
				tmplist.append(atom)

		self.atomlist = tmplist



	def selectElement(self):

		"""
		select atoms that have a given element
		"""

		if len(self.element) == 0:
			return

		tmplist = []
		for atom in self.atomlist:
			found = False
			for element in self.element:
				if atom.element == element:
					found = True

			if found and not self.invelement:
				tmplist.append(atom)
			if not found and self.invelement:
				tmplist.append(atom)

		self.atomlist = tmplist



	def selectType(self):

		"""
		select atoms that are of a given type (HETATM vs ATOM)
		"""

		if len(self.type) == 0:
			return

		tmplist = []
		for atom in self.atomlist:
			found = False
			for type in self.type:
				if atom.kind == type:
					found = True	

			if found and not self.invtype:
				tmplist.append(atom)
			if not found and self.invtype:
				tmplist.append(atom)

		self.atomlist = tmplist
		

					
	def assembleMol(self):

		"""
		assemble a molecule from a list of atoms
		"""

		newMol = Molecule()

		for atom in self.atomlist:
			res   = atom.parentResidue
			chain = res.parentChain

			currChain = newMol.getChain(chain.name)
			if not currChain:
				currChain = newMol.newChain()
				currChain.copy(chain)


			currRes = currChain.getResidue(res.file_id)
			if not currRes:
				currRes = currChain.newResidue()
				currRes.copy(res)

			currRes.addAtom(atom)

		return newMol



class macro_selection:

	def __init__(self):
		self.selection = Selection()
		self.type      = "around"
		self.cutoff    = 6.0


	def apply_selection(self, mol=None, atmlist=None):

		origlist = atmlist
		for macro in self.selection.macros:
			if mol != None:
				small_list = macro.apply_selection(atmlist=mol.atomList())
			elif atmlist != None:
				small_list = macro.apply_selection(atmlist=atmlist)

		newmol = self.selection.apply_selection(atmlist=atmlist)
		newlist = newmol.atomList()

		return_list = []
		if self.type == "expand":
			return_list = atomsAroundAtoms(atms=newlist, atomList=origlist, cutoff=self.cutoff)
		elif self.type == "around":
			tmp_list = atomsAroundAtoms(atms=newlist, atomList=origlist, cutoff=self.cutoff)
			for atm in tmp_list:
				if atm in newlist:
					continue
				return_list.append(atm)
		else:
			return_list = newlist

		return return_list
		

