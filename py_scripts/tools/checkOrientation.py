#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from Molecule import *
from Selection import *

def main():

	"""
WARNING: NOT A GENERALIZED SCRIPT
This script is hard coded for the kemp substrate
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
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
	for pdbfile in pdbfiles:
		print pdbfile,
		protein.readPDB(pdbfile)
		# --- hack for now
		A = protein.getAtom(9004)
		B = protein.getAtom(9014)
		C = protein.getAtom(9015)

		az = A.coord.z
		bz = B.coord.z
		cz = C.coord.z

		if az > bz and az > cz:
			print "  DOWN"
		else:
			print "  UP"
			

		
		protein.clear()




if __name__ == "__main__":
	main()
