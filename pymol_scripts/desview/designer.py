from pymol import cmd
from Enzyme import *
from Resfile import *

class designer:

	"""
	class for designing with pymol
	"""

	def __init__(self):
		self.resfile = Resfile()
		self.mol     = None



	def setMolecule(self, mol=None):
		if mol == None:
			print "usage: setMolecule(mol)"
			return

		self.mol = mol
		self.resfile.setMolecule(mol)
		


	def setRepackable(self):

		"""
		takes the current selection and sets the residues to be repackable
		"""

		# --- update residue names --- #

		mylist = residuesInSelection("sele")
		print mylist

