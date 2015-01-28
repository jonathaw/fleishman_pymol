sys.path.append("/Users/sarelf/python_scripts/pymol_scripts/desview/")
sys.path.append("/Users/sarelf/python_scripts/py_scripts")

from pymol.wizard import Wizard
from pymol import cmd
from design_viewer import *
import pymol
from types import *
from Resfile import *
from wizard_rosetta import *
from rosetta_engine import *




class wizard_desview(Wizard):

	def launch(self, name):
		return None

	
	def __init__(self):

		Wizard.__init__(self)
		self.viewer = design_viewer()
		self.resfile = Resfile()

		sess = cmd.get_session()
		base = ""
		for i in sess["names"]:
			if type(i) is ListType:
				base = i[0]

		if base != "":
			self.setDesigned(base)

		self.wiz_ros = wizard_rosetta()
			


	def get_panel(self):
		return [
			[1, 'design', ''],
			[2, 'set designed', 'cmd.get_wizard().setDesigned()'],
			[2, 'set native' , 'cmd.get_wizard().setNative()'],
			[2, 'show substitutions', 'cmd.get_wizard().showSubs()'],
			[2, 'hide substitutions', 'cmd.get_wizard().hideSubs()'],
			[2, 'unsatisfied hbonds', 'cmd.get_wizard().showUHB()'],
			[2, 'show res score', 'cmd.get_wizard().res_score()'],
			[2, 'list clashes', 'cmd.get_wizard().showClashes()'],
			[2, 'mutate', 'cmd.get_wizard().mutate()'],
			[2, 'holes', 'cmd.get_wizard().holes()'],
			[2, 'save', 'cmd.get_wizard().savePDB()'],
		]


	def res_score(self):

		"""
		reports the rosetta score for the residue
		"""

		reslist = residuesInSelection("sele")	
		if len(reslist) != 1:
			print "only select 1 residue"
			return

		myres = self.viewer.design.getResidue(reslist[0])
		if myres == None:
			print "unable to locate residue"
			return

		print "Residue:",myres.name,myres.file_id," Erep = ",myres.Erep," Eatr = ",myres.Eatr," EhbSC = ",myres.EhbSC


	def holes(self):

		cmd.delete("_packing")
		file = self.viewer.design.file
		binary = "trunk.mactel"
		args   = " -pose1 -fa_input -fa_output -nstruct 1 -enable_ligand_aa -cst_mode -make_packing_pdb -no_optH -overwrite -s "
		exe = binary + args + file
		base = file.split(".")
		newfile = base[0] + "_packing.pdb"
		os.system(exe)
		cmd.load(newfile, "_packing")
		cmd.hide("lines", "_packing")


	def showClashes(self, cutoff=3.0):

		Erep = self.viewer.design.Erep
		clashes = []
		for chn in self.viewer.design:
			for res in chn.residue:
				if res.Erep > cutoff:
					clashes.append(int(res.file_id))

		print "clashes:"
		print clashes



	def mutate(self):

		self.wiz_ros.setMolecule(self.viewer.design, "designed")
		self.wiz_ros.startup()
		self.wiz_ros.des_view = self.viewer
		cmd.set_wizard(self.wiz_ros)


	def showSubs(self):
		self.viewer.displaySubstitutions()


	def hideSubs(self):
		self.viewer.displayNormal()



	def setDesigned(self, base=""):
		
		# --- get last structure --- #
		if base == "":
			sess = cmd.get_session()
			for i in sess["names"]:
				if type(i) is ListType:
					base = i[0]

		file = base + ".pdb"
		cmd.set_name(base, "designed")
		self.viewer.setDesign(file)
		self.viewer.selectCatalytic()
		self.viewer.displayDesigned()


	def setNative(self, base=""):

		# --- get last structure --- #
		if base == "":
			sess = cmd.get_session()
			for i in sess["names"]:
				if type(i) is ListType:
					base = i[0]

		cmd.set_name(base, "native")
		file = base + ".pdb"
		self.viewer.setNative(file)
		self.viewer.displayNative()



	def loadResfile(self, file=""):

		self.resfile.read(file)
		des = self.resfile.designedResidues()
		rep = self.resfile.repackedResidues()

		pdes = []
		for i in des:
			pdes.append(str(i))

		prep = []
		for i in rep:
			prep.append(str(i))

		des_sele = string.join(pdes, ",")
		rep_sele = string.join(prep, ",")


		if len(des_sele) > 0:
			cmd.select("designable", "(resi " + des_sele + ")")

		if len(rep_sele) > 0:
			cmd.select("repackable", "(resi " + rep_sele + ")")
		cmd.disable("repackable")



	def showUHB(self):

		self.viewer.unsat()


	def savePDB(self, file="pymol_output.pdb"):

		self.viewer.design.writePDB(file)

		
