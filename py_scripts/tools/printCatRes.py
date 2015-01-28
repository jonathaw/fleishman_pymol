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
	prints the catalytic residues in the pdbfile
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-d", dest="dash",    help="dash", action="store_true")
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
	med = ""
	if options.dash:
		med = "-"
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		cat = getCatalyticResidues(protein)	

		print pdbfile,
		mystring = ""
		for c in cat:
			mystring += c.name + med + c.file_id.strip() + "_"
		print mystring
		protein.clear()




if __name__ == "__main__":
	main()
