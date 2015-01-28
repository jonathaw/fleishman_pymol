#!/usr/bin/python

from Molecule import *
from Selection import *
from optparse import OptionParser
import sys, string


def main():

	"""
creates a poly-glycine variant of a pdbfile by removing all sidechains
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.pdbfile or not options.outfile:
		parser.print_help()
		sys.exit()
		
	selection = Selection()	
	selection.makeSelection("BB")

	protein = Molecule()
	protein.readPDB(options.pdbfile)
	newmol  = selection.apply_selection(protein)
	for chain in newmol.chain:
		for res in chain.residue:
			res.name = "GLY"

	newmol.writePDB(options.outfile)



if __name__ == "__main__":
	main()

