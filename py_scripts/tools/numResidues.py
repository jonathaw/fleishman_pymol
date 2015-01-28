#!/usr/bin/python

import sys, os, string
from optparse import OptionParser
from Molecule import *
from file_routines import *



def main():

	"""
reports the number of residues in a pdbfile
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-t", dest="type", help="residue type")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()	


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
		protein.readPDB(pdbfile)
		if options.type:
			ntype = 0
			for chain in protein.chain:
				for res in chain.residue:
					if res.name == options.type:
						ntype += 1
			ans = pdbfile + ": " + str(ntype)
		else:
			ans = pdbfile + ": " + str(protein.numResidues())

		print ans
		protein.clear()



if __name__ == "__main__":
	main()

	
