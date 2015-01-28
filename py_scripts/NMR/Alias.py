#!/usr/bin/python


"""

	Alias.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import string


class Alias:

	"""
	class used to setup atom alias names
	"""

	def __init__(self):
		self.res_alias  = {}
		self.atom_alias = {}


	def read(self,file):

		"""
		reads in an alias file in its own format
		"""

		try:
			FILE = open(file)
		except:
			print "unable to open file"
			sys.exit()

		for line in FILE.readlines():
			line = string.rstrip(line)
			if len(line) > 4:
				cols = line.split()

			if cols[0] == "RESIDUE":
				resa = cols[3].split(",")	
				self.res_alias[cols[1]] = resa

			if cols[0] == "ATOM":
				rname = cols[1]
				aname = cols[2]
				atma  = cols[4].split()

				# ---   check to see if residue name is an alias   --- #
				if rname in self.res_alias.keys():
					for res in self.res_alias[rname]:
						if not res in self.atom_alias.keys():
							self.atom_alias[res] = {}
						
						self.atom_alias[res][aname] = atma
				else:
					if not rname in self.atom_alias.keys():
						self.atom_alias[rname] = {}

					self.atom_alias[rname][aname] = atma

		FILE.close()
							


	def getAlias(self, resn, atomn):

		"""
		returns the alias for an atom belonging to a given residue
		"""

		if not resn in self.atom_alias.keys():
			return None

		for alias in self.atom_alias[resn].keys():
			if atomn in self.atom_alias[resn][alias]:
				return alias
