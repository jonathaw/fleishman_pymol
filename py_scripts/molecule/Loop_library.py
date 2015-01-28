#!/usr/bin/python


"""

	Loop_library.py

	stores a list of loops

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


from Molecule import *



class Loop_library:


	def __init__(self):
		self.molecule = Molecule()
		self.nmodels  = 0
		self.start_point = 0
		self.end_point = 0
		self.length    = 0



	def display(self):
		
		"""
		returns a string containing loop information
		"""

		repr = "#models: " + str(self.nmodels) + "; start_point: " + str(self.start_point) + "; end_point: " + str(self.end_point)

		return repr



	def __repr__(self):

		"""
		prints the atom information
		"""
	
		repr = self.display()
		return repr


	def read(self, file):	
		
		"""
		reads in a loop library
		"""

		self.molecule.readPDB(file)

		re_nloop = re.compile("REMARK_NLOOPS")
		re_length = re.compile("REMARK_LOOP_LENGTH")
		for rem in self.molecule.remark:
			cols = rem.split()
			if re_nloop.match(rem):
				self.nmodels = int(cols[1])
			if re_length.match(rem):
				self.length = int(cols[1])

		if self.molecule.numChains() != self.nmodels:
			print "difference in number of models"
			print "header:",self.nmodels
			print "file:",self.molecule.numChains()
			sys.exit()



	def getLoop(self,index):

		if index < 0 or index >= self.nmodels:
			print "accessing loop out of bounds"
			sys.exit()

		# return a clone of the chain instead
		clone_chain = self.molecule.chain[index].clone()

		return clone_chain



	def addLoop(self,reslist):

		mychain = self.molecule.newChain()
		mychain.addResidueList(reslist)
