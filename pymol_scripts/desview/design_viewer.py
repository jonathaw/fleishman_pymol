from pymol import cmd
from Enzyme import *
from design_routines import *
from match_routines import *
from mol_routines import *
from surface_routines import *
from Hbond import *
from rosetta_engine import *
from rosetta_visualize import *
sys.path.append("/Users/sarelf/python_scripts/pymol_scripts")

from pymol_scripts import *
from InterfaceUtils import loadInterfacePDB
import string

class design_viewer:

	"""
	class for displaying designed enzymes
	"""

	def __init__(self):
		self.design = Enzyme()
		self.native = Molecule()
		useRosettaRadii()
		#cmd.set("seq_view", 1)
		#cmd.set("seq_view_label_mode", 3)
		self.nativeFile = ""
		self.designFile = ""
		self.rosetta = rosetta_engine()
		self.rosetta.setMolecule(self.design)



	def setNative(self, file):

		"""
		sets the native structure
		"""

		self.native.clear()
		self.native.readPDB(file)
		self.nativeFile = file



	def setDesign(self, file):
		
		"""
		sets the designed structure
		"""

		self.design.clear()
		self.design.readPDB(file)
		self.designFile = file

		lig = self.design.ligand
		if lig == None:
			return

		print "LIGAND: Erep = ",lig.Erep,"Eatr = ",lig.Eatr,"EhbSC = ",lig.EhbSC



	def loadDesign(self, file):

		"""
		loads the designed structure
		"""

		loadInterfaceDesign(file, "designed")
		self.setDesign(file)




	def loadNative(self, file):

		"""
		loads the native structure
		"""

		myview = cmd.get_view()
		cmd.load(file, "native")
		self.setNative(file)
		self.displayNative()
		cmd.set_view(myview)



	def getSubstitutions(self):

		"""
		returns a list of substituted residues
		"""

		native_sequence = self.native.sequence()
		design_sequence = self.design.protein.sequence()

		slist = getSubstitutionPositions(native_sequence, design_sequence)
		wordlist = []
		for i in slist:
			wordlist.append(str(i))
		
		diff_list = string.join(wordlist, ",")
		print diff_list
		cmd.select("desres", "(resi " + diff_list + ")")
		cmd.disable("desres")



	def selectCatalytic(self,mol=None, sele="all"):
		
		"""
		selects catalytic residues in the designed protein
		"""

		if mol == None:
			mol = self.design

		cat = []
		for c in mol.catalytic:
			cat.append(int(c.file_id))

		if len(cat) > 0:
			strcat = []
			for i in cat:
				strcat.append(str(i))

			mylist = string.join(strcat, ",")
			cmd.delete("catalytic")
			cmd.select("catalytic", "(" + sele + " & resi " + mylist + ")")
			cmd.disable("catalytic")
		else:
			print "no catalytic residues"



	def displaySubstitutions(self):

		"""
		displays substitutions
		"""

		if self.native.numResidues() == 0:
			return

		view = cmd.get_view()
		self.getSubstitutions()
		print "here1"
		cmd.select("_nearbynat", "native & (byres ligand around 9.0)")
		cmd.color("violet", "designed & element C & desres & !catalytic")
		cmd.color("cyan", "native & element C & desres")
		cmd.color("violet", "native & name CA & desres")
		print "made it here"
		#cmd.show("lines", "_nearbynat")
		displayLines("_nearbynat")
		cmd.set_view(view)


	
	def displayNormal(self):

		"""
		display normal (no substitutions)
		"""

		if self.native.numResidues() != 0:
			cmd.hide("lines", "native")

		view = cmd.get_view()
		self.displayDesigned()
		cmd.set_view(view)



	def displayNative(self):

		"""
		displays the native protein
		"""

		cmd.hide("lines", "native")
		cmd.color("gray", "native & name CA")
		#cmd.zoom("nearby")



	def displayDesigned(self, selection="designed", mol=None):

		"""
		displays the designed protein
		"""

		if mol == None:
			mol = self.design

		cmd.remove("name AX*")
		cmd.remove("name CEN*")
		cmd.remove("name CONT")

		cmd.hide("lines", selection)
		cmd.show("cartoon", selection)

		cmd.select("ligand", selection + " & HETATM & !name V*")
		cmd.select("virtual", selection + " & HETATM & name V*")
		cmd.select("protein", selection + " & !HETATM")
		cmd.select("shell1", "protein & (byres ligand around 5.0)")
		cmd.select("nearby", "protein & (byres ligand around 9.0)")
		cmd.disable("nearby")
		
		cmd.color("gray", selection + " & name CA")
		cmd.color("magenta", "virtual")
		cmd.color("tv_green", "element C & protein & !name CA")
		displayLigand("ligand")

		
		if mol.numCatalytic() > 0:
			cmd.color("brightorange", "catalytic & element C")
			cmd.show("stick", "catalytic")
			cmd.set("stick_radius", 0.2, "catalytic")
		else:
			print "no catalytic residues"

		displaySticks("shell1")
		displayLines("nearby")
		cmd.do("show_ligand_holes(0.8)")
		#cmd.do("ligandMesh")
		cmd.zoom("nearby")
		


	def displayMutation(self, sele):

		cmd.hide("lines", sele)
		cmd.select("_ligand2", "HETATM & !name V* &" + sele)
		cmd.select("_protein2", "!HETATM &" + sele)
		cmd.select("_nearby2", "_protein2 & (byres _ligand2 around 9.0)")

		cmd.color("slate", "element C & !HETATM & " + sele)
		cmd.color("gray", "name CA & " + sele)
		#cmd.show("sticks", "_nearby2")
		displaySticks("_nearby2")

		if self.design.numCatalytic() > 0:
			cmd.color("brightorange", "catalytic & element C")

		#cmd.show("spheres", "_ligand2")
		displayLigand("_ligand2")
		cmd.show("cartoon", sele)
		cmd.zoom("_nearby2")
		

	def unsat(self):

		"""
		gets unsatisfied Hbonds in the designed
		"""

		nearlist = residuesAroundAtoms(self.design.ligand.atom, self.design,12.0)
		HBN = HBnetwork()	
		HBN.createNetwork(reslist=nearlist)
		HBN.findHbonds()
		unsat = HBN.unsatisfiedHbonds()

		ids = []
		Taken = {}
		mysel = cmd.get_model("nearby")
		natom = len(mysel.atom)
		for i in range(natom):
			Taken[mysel.atom[i].resi] = True

			mylist = []
			for i in Taken.keys():
				mylist.append(int(i))

		mylist.sort()

		get_surface_area(self.designFile, "surf")
		surfMol = Molecule()
		surfMol.readPDB("surf.asa")
		if len(surfMol.chain) == 0:
			print "surface area script not working ..."
			print "aborting"
			return

		for atm in unsat:
			print atm
			if int(atm.resi) in mylist:
				myres = surfMol.getResidue(atm.resi)
				myatm = myres.getAtom(atm.name)
				if myatm.occupancy < 4.0:
					if not HBN.containsAtom(atm):
						ids.append(str(int(atm.file_id)))

						if len(ids) > 100:
							print "over 100"
							break

		ids = string.join(ids, ",")	
		mysel = "designed & (id " + ids + ")"
		cmd.create("_unsatisfied", mysel)
		cmd.set("sphere_scale", 0.25, "_unsatisfied")
		cmd.show("spheres", "_unsatisfied")
		cmd.color("hotpink", "_unsatisfied")

		HBN.clear()



	def setRepackable(self, selection=""):

		"""
		sets repackable residues
		"""

		self.rosetta.setRepackable("sele")



	def showRepackable(self):

		"""
		shows repackable residues
		"""

		repacked = self.rosetta.resfile.repackedResidues()
		activelist = []
		for i in repacked:
			activelist.append(str(i))

		print activelist

		mylist = string.join(activelist, ",")
		mylist = "(resi " + mylist + ")"
		cmd.color("yellow", mylist)
		


	def runRosetta(self):

		self.rosetta.run()
		# hack for now to transfer catalytic residues
		catres = []
		for c in self.design.catalytic:
			catres.append(int(c.file_id))

		#cmd.delete("designed")
		cmd.load("design_design.pdb", "designed2")
		self.setDesign("design_design.pdb")

		for c in catres:
			res = self.design.getResidue(c)
			self.design.catalytic.append(res)

		self.selectCatalytic()
		self.displayMutation("designed2")
