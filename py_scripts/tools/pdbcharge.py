#!/usr/bin/python


import os, sys, string
from optparse import OptionParser
from Molecule import *


def main():
	
	"""
reports the formal charge of a pdbfile where ASP/GLU are -1 and LYS/ARG are +1
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.pdbfile:
		parser.print_help()
		sys.exit()

	protein = Molecule()
	protein.readPDB(options.pdbfile)

	charge = 0.0
	for chain in protein.chain:
		for residue in chain.residue:
			if residue.name == "ASP" or residue.name == "GLU":
				charge -= 1.0
			if residue.name == "LYS" or residue.name == "ARG":
				charge += 1.0

	print ("Charge = %5.1f" % charge)




if __name__ == "__main__":
	main()
