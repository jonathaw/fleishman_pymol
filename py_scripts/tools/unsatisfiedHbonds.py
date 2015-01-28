#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Molecule import *
from Selection import *
from Hbond import *

def main():

	"""
prints a list of unsatisfied hydrogen bonds in a protein
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile",   help="pdbfile")
	parser.add_option("-P", dest="pdblist",   help="pdblist")
	parser.add_option("-s", dest="selection", help="selection")
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

	protein = Molecule()
	HBN = HBnetwork()

	sele = None
	if options.selection:
		sele = Selection()
		sele.makeSelection(options.selection)
		
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		HBN.createNetwork(protein)
		HBN.findHbonds()
		unsat = HBN.unsatisfiedHbonds()

		if options.selection:
			atmlist = sele.apply_selection(protein,return_mol=False)
			for atm in unsat:
				if atm in atmlist:
					print atm
		else:
			for atm in unsat:
				print atm

		protein.clear()
		HBN.clear()




if __name__ == "__main__":
	main()
