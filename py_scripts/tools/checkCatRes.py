#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Molecule import *
from Selection import *

def main():

	"""
not a very generalized script.  This double checks the number of residues in chain B which
for a mabo-formatted pdbfile is the number of catalytic residues
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-n", dest="number", help="number")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	if not options.number:
		parser.print_help()
		sys.exit()
	

	protein = Molecule()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		chainB = protein.getChain("B")
		if chainB == None:
			print "ERROR! chain B not found"
			print "file may not be mabo-formatted"
			sys.exit()

		if chainB.numResidues() != int(options.number):
			print pdbfile
		protein.clear()




if __name__ == "__main__":
	main()
