#!/usr/bin/python

from Molecule import *
from Selection import *
from optparse import OptionParser
import sys, string


def main():

	"""
creates a poly-alanine variant of a given pdbfile by just keeping the CB's from sidechains
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
	selection.makeSelection("CEN")

	protein = Molecule()
	protein.readPDB(options.pdbfile)
	newmol  = selection.apply_selection(protein)
	for chain in newmol.chain:
		for res in chain.residue:
			if res.name != "GLY":
				res.name = "ALA"

	newmol.writePDB(options.outfile)



if __name__ == "__main__":
	main()

