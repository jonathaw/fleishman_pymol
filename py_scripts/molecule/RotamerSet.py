#!/usr/bin/python


"""

	RotamerSet.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


from Rotamer import *


class RotamerLibrary:

	"""
	class for storing libraries of rotamers
	"""
	
	def __init__(self):
		self.residue = {}
		self.residue["ALA"] = RotamerSet("ALA")
		self.residue["CYS"] = RotamerSet("CYS")
		self.residue["ASP"] = RotamerSet("ASP")
		self.residue["GLU"] = RotamerSet("GLU")
		self.residue["PHE"] = RotamerSet("PHE")
		self.residue["GLY"] = RotamerSet("GLY")
		self.residue["HIS"] = RotamerSet("HIS")
		self.residue["ILE"] = RotamerSet("ILE")
		self.residue["LYS"] = RotamerSet("LYS")
		self.residue["LEU"] = RotamerSet("LEU")
		self.residue["MET"] = RotamerSet("MET")
		self.residue["ASN"] = RotamerSet("ASN")
		self.residue["PRO"] = RotamerSet("PRO")
		self.residue["GLN"] = RotamerSet("GLN")
		self.residue["ARG"] = RotamerSet("ARG")
		self.residue["SER"] = RotamerSet("SER")
		self.residue["THR"] = RotamerSet("THR")
		self.residue["VAL"] = RotamerSet("VAL")
		self.residue["TRP"] = RotamerSet("TRP")
		self.residue["TYR"] = RotamerSet("TYR")

		self.stdev = 1.0



	def allowed(self,resname="",phi=0.0,psi=0.0,chi1=0.0,chi2=0.0,chi3=0.0,chi4=0.0):

		"""
		checks to see if a rotamer in the set matches up with a set of given values
		"""

		myset = self.residue[resname]

		if len(myset.data) == 0:
			return True

		# --- bin the phi psi --- #
		phinc = 5.0
		psinc = 5.0
		if phi < 0:
			phinc = -5.0

		if psi < 0:
			psinc = -5.0

		phi = int((phi+phinc)/10.0)*10.0
		psi = int((psi+psinc)/10.0)*10.0

		for rot in myset.data:
			if rot.matches(phi,psi,chi1,chi2,chi3,chi4):
				return True

		return False



	def setStdev(self, stdev):

		"""
		set the std deviation used
		"""

		self.stdev = stdev



	def read(self, file):

		"""
		reads a dunbrak library
		"""

		try:
			FILE = open(file)
		except:
			print "unable to open file:",file
			return

		for line in FILE:	
			cols = line.split()
			if len(cols) > 1:
				rot = self.residue[cols[0]].newRotamer()
				
				rot.phi = float(cols[1])
				rot.psi = float(cols[2])

				rot.chi1 = float(cols[9]) + 180.0
				rot.chi2 = float(cols[10]) + 180.0
				rot.chi3 = float(cols[11]) + 180.0
				rot.chi4 = float(cols[12]) + 180.0

				rot.stdev1 = self.stdev*float(cols[13])
				rot.stdev2 = self.stdev*float(cols[14])
				rot.stdev3 = self.stdev*float(cols[15])
				rot.stdev4 = self.stdev*float(cols[16])



	
class RotamerSet:

	"""
	storage class for storing rotamers
	"""

	def __init__(self, name=""):
		self.data = []
		self.name = name

	def newRotamer(self):
		rot = Rotamer()
		self.data.append(rot)

		return rot

	def display(self):
		for rot in self.data:
			rot.display()
				

