#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from Molecule import *
from Selection import *

def main():

	"""
	switches tautomers of histidine in a selection of residues
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-s", dest="selection", help="selection")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.pdbfile:
		parser.print_help()
		sys.exit()

	if options.outfile:
		outfile = options.outfile
	elif options.replace:
		outfile = options.pdbfile
	else:
		parser.print_help()
		sys.exit()

	sele = Selection()
	if options.selection:
		sele.makeSelection(options.selection)
	else:
		sele.makeSelection("resn=HIS")
	
	protein = Molecule()
	protein.readPDB(options.pdbfile)

	his_prot = sele.apply_selection(protein)
	his_list = his_prot.residueList()

	for his in his_list:
		switchHisTautomer(his)

	protein.writePDB(outfile,resRenumber=False,atomRenumber=False)



if __name__ == "__main__":
	main()
