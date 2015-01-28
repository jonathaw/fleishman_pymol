#!/usr/bin/python


"""

	Hbond.py

	Hydrogen bonding class

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import math,os,string
import xml.dom.minidom
from Molecule import *
from mol_routines import *




def HBenergy(D=None, H=None, A=None, AA=None, donor=None, acceptor=None):

	"""
	returns the hydrogen bonding energy
	"""

	if donor != None:
		D = donor.D
		H = donor.H

	if acceptor != None:
		A  = acceptor.A
		AA = acceptor.AA

	dist = H.distance(A) - 2.0
	HBE = 0.0
	if dist < 2.0:
		ang1 = vector3d.angle3(H.coord,A.coord,AA.coord)
		if ang1 > 100.0:
			ang2 = vector3d.angle3(D.coord,H.coord,A.coord)
			ang2 = math.radians(ang2)
			cos2 = math.cos(ang2)
			HBE = -1.0*(cos2*cos2)*math.exp(-1.0*dist*dist)

	return HBE



def HBenergy1(D=None, H=None, A=None):

	"""
	returns the hydrogen bonding energy with no acceptor antecedant
	"""

	dist = H.distance(A) - 2.0
	HBE = 0.0
	if dist < 2.0:
		ang2 = vector3d.angle3(D.coord,H.coord,A.coord)
		ang2 = math.radians(ang2)
		cos2 = math.cos(ang2)
		HBE = -1.0*(cos2*cos2)*math.exp(-1.0*dist*dist)

	return HBE





class HBnetwork:

	"""
	class used for storing all hydrogen bonds
	"""

	def __init__(self, HBdef=None):

		if HBdef == None:
			HBdef = HBdefinitions()
			HBdef.read()

		self.definitions = HBdef
		self.donors      = []
		self.acceptors   = []
		self.hbonds      = []



	def clear(self):

		"""
		clears the donors and acceptors
		"""

		self.donors = []
		self.acceptors = []
		self.hbonds = []



	def numDonors(self):
		
		"""
		returns the number of donors
		"""

		return len(self.donors)



	def numAcceptors(self):
		
		"""
		returns the number of acceptors
		"""

		return len(self.acceptors)



	def numHbonds(self):
		
		"""
		returns the number of hydrogen bonds
		"""
	
		return len(self.hbonds)



	def newDonor(self, D=None, H=None, type="", res=None):

		"""
		creates a new donor object
		"""

		myD = HBdonor(D,H,type,res)
		self.donors.append(myD)
		return myD



	def newAcceptor(self, A=None, AA=None, type="", res=None):

		"""
		creates a new acceptor object
		"""

		myA = HBacceptor(A,AA,type,res)
		self.acceptors.append(myA)
		return myA



	def newHbond(self, donor=None, acceptor=None):
		
		"""
		creates a new hbond between a donor and acceptor
		"""

		hb = Hbond(donor=donor, acceptor=acceptor)
		self.hbonds.append(hb)
		return hb



	def createNetwork(self, molecule=None, reslist=None):
	
		"""
		creates a HBond network by identifying donors and acceptors in the molecule
		"""

		if molecule == None and reslist == None:
			return

		if molecule != None:
			reslist = molecule.residueList()

		for res in reslist:
			if res == None:
				print "no residue"
				return

			t = self.definitions.getTemplate(res.name)

			# get generic residue template
			if t == None:
				# find donors
				getRosettaElement(res=res)
				for atm in res.atom:
					if atm.element == "H":
						neigh = bondedNeighbors(res=res,atm=atm,cutoff=1.4)
						if len(neigh) == 1:
							if neigh[0].element == "N" or neigh[0].element == "O":
								self.newDonor(neigh[0],atm,"sidechain",res)

				# find acceptors
				for atm in res.atom:
					if atm.element == "N" or atm.element == "O":
						neigh = bondedNeighbors(res=res,atm=atm,cutoff=2.0)
						if len(neigh) == 0 or len(neigh) >= 4:
							continue

						this_aa = None
						for nei in neigh:
							if nei.element != "H":
								this_aa = nei
								break

						if this_aa == None:
							continue

						self.newAcceptor(atm,this_aa,"sidechain",res)
				continue

			for donor in t.donors:
				d = res.getAtom(donor.D)
				h = res.getAtom(donor.H)

				if d == None or h == None:
					#print "cannot find donor atoms",donor.D,donor.H,res.name,res.file_id
					#print res
					continue

				self.newDonor(d,h,donor.type,res)

			for acceptor in t.acceptors:
				a  = res.getAtom(acceptor.A)
				aa = res.getAtom(acceptor.AA)

				if a == None or aa == None:
					#print "cannot find acceptor atoms"
					#print res
					continue

				self.newAcceptor(a,aa,acceptor.type,res)



	def findHbonds(self, cutoff=-0.3,function=0):

		"""
		finds hydrogen bonds in the network based on their energies
		"""

		for donor in self.donors:
			for acceptor in self.acceptors:
				# for now no self bonds 
				if acceptor.res == donor.res:
					continue

				e = 0.0
				if function == 1:
					e = HBenergy1(donor.D, donor.H, acceptor.A)
				else:
					e = HBenergy(donor=donor, acceptor=acceptor)
				if e < cutoff:
					hb = self.newHbond(donor, acceptor)
					hb.energy = e



	def HbondExists(self, residue1=None, residue2=None):
		
		"""
		checks to see if two residues are Hbonded
		"""

		if residue1 == None or residue2 == None:
			return False

		for hb in self.hbonds:
			if hb.donor.res == residue1 and hb.acceptor.res == residue2:
				return True
			if hb.donor.res == residue2 and hb.acceptor.res == residue1:
				return True

		return False

	def unsatisfiedHbonds(self):

		"""   
		returns a list of unsatisfied hydrogen bonds
		"""      
               
		unsat = []
		for donor in self.donors:
			found = False
			for hb in self.hbonds:
				if donor == hb.donor:
					found = True
					break

			if not found:
				unsat.append(donor.D)


		for acceptor in self.acceptors:
			found = False
			for hb in self.hbonds:
				if acceptor == hb.acceptor:
					found = True
					break

			if not found:
				unsat.append(acceptor.A)

		return unsat



	def getHbondsToResidue(self, myres=None):
		
		"""
		returns a list of hydrogen bonds being made to a given ligand
		"""

		hbs = []
		for hb in self.hbonds:
			if hb.donor.res == myres or hb.acceptor.res == myres:
				hbs.append(hb)

		return hbs


	def containsAtom(self, atm=None):

		"""
		checks to see if hydrogen bond network contains an atom
		"""
	
		for hb in self.hbonds:
			if hb.containsAtom(atm):
				return True

		return False




class Hbond:

	"""
	hydrogen bond class
	"""

	def __init__(self, donor=None, acceptor=None):
		self.donor    = donor
		self.acceptor = acceptor
		self.energy   = 0.0



	def __repr__(self):

		aaname = "    "
		if self.acceptor.AA != None:
			aaname = self.acceptor.AA.name

		repr = ('%3s%4i %4s %4s %4i -> %3s%4i %4s %4s %4i  %8.3f' %
					(self.donor.res.name, int(self.donor.res.file_id), self.donor.D.name, self.donor.H.name, int(self.donor.D.file_id), self.acceptor.res.name, int(self.acceptor.res.file_id), self.acceptor.A.name,  aaname, int(self.acceptor.A.file_id), self.energy))

		return repr


	def containsAtom(self, atm=None):

		"""
		checks to see in a hydrogen bond contains an atom
		"""

		if atm == None:
			return False

		if self.acceptor.A == atm or self.acceptor.AA == atm:
			return True

		if self.donor.D == atm or self.donor.H == atm:
			return True

		return False



class HBacceptor:

	"""
	hydrogen bond acceptor class
	"""

	def __init__(self, A=None, AA=None, type="", res=None):
		self.A    = A
		self.AA   = AA
		self.res  = res
		self.type = type





class HBdonor:

	"""
	hydrogen bond donor class
	"""
	
	def __init__(self, D=None, H=None, type="", res=None):
		self.D    = D
		self.H    = H
		self.res  = res
		self.type = type
				
					
		

class HBdefinitions:

	"""
	definitions class used to read, identify, and store hydrogen bonds in molecules
	"""

	def __init__(self):

		home = os.environ["pyScriptsDir"]
		self.file = home + "/data/hbond.xml"
		self.templates = []



	def newTemplate(self, name=""):

		"""
		creates and returns a new template object
		"""

		t = HBtemplate(name)
		self.templates.append(t)
		return t



	def getTemplate(self, name=""):

		"""
		returns a template with a given name
		"""

		for t in self.templates:
			if t.name == name:
				return t

		return None



	def templateExists(self, name=""):

		"""
		checks to see if a template residue exists
		"""

		for t in self.templates:
			if t.name == name:
				return True

		return False



	def numTemplates(self):

		"""
		returns the number of template residues
		"""

		return len(self.templates)



	def read(self, file=""):

		"""
		reads hydrogen bond information from an XML file
		"""

		if file == "":
			file = self.file

		mydoc = xml.dom.minidom.parse(file)

		aliases = {}
		for e in mydoc.childNodes:
			if e.nodeType == e.ELEMENT_NODE and e.localName == "list":

				for n in e.childNodes:

					# --- read aliases --- #
					if n.nodeType == n.ELEMENT_NODE and n.localName == "residue_alias":
						orig = n.getAttribute("original")
						alis = n.getAttribute("alias")
						if not orig in aliases:
							aliases[orig] = alis
						

					# --- read residues --- #
					if n.nodeType == n.ELEMENT_NODE and n.localName == "residue":
						name = n.getAttribute("identity")
						res = self.getTemplate(name)
						if res == None:
							res = self.newTemplate(name)

								
						for h in n.childNodes:
							if h.nodeType == h.ELEMENT_NODE and h.localName == "hbond":
								type = h.getAttribute("type")
								for d in h.childNodes:
									if d.nodeType == d.ELEMENT_NODE and d.localName == "donor":
										don = d.getAttribute("D")
										hyd = d.getAttribute("H")
										res.newDonor(don, hyd, type)
									if d.nodeType == d.ELEMENT_NODE and d.localName == "acceptor":
										acc = d.getAttribute("A")
										aaa = d.getAttribute("AA")
										res.newAcceptor(acc, aaa, type)

						# check for aliases #
						for key in aliases.keys():
							if aliases[key] == name:
								tmpres = self.getTemplate(key)
								if tmpres == None:
									tmpres = self.newTemplate(key)

								for acc in res.acceptors:
									tmpres.newAcceptor(acc.A, acc.AA, acc.type)
								for don in res.donors:
									tmpres.newDonor(don.D, don.H, don.type)
										




class HBtemplate:

	"""
	class for holding information of atoms involved in hydrgoen bonds in a residue
	"""

	def __init__(self, name=""):
		self.donors    = []
		self.acceptors = []
		self.name      = name



	def newDonor(self, D="", H="", type=""):

		"""
		creates and returns a new donor object
		"""

		don = HBdonor_template(D,H,type)
		self.donors.append(don)
		return don



	def newAcceptor(self, A="", AA="", type=""):

		"""
		creates and returns a new acceptor object
		"""

		acc = HBacceptor_template(A,AA,type)
		self.acceptors.append(acc)
		return acc



	def numDonors(self):

		"""
		returns the number of donors in an object
		"""

		return len(self.donors)



	def numAcceptors(self):

		"""
		returns the number of acceptors in an object
		"""

		return len(self.acceptors)





class HBdonor_template:

	"""
	donor class holds information on the names of atoms
	"""

	def __init__(self, D="", H="", type=""):
		self.D = D
		self.H = H
		self.type = type





class HBacceptor_template:

	"""
	acceptor class holds information on the names of atoms
	"""

	def __init__(self, A="", AA="", type=""):
		self.A  = A
		self.AA = AA
		self.type = type

