#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from Molecule import *
from optparse import OptionParser
import os, string, sys



def main():

	"""
lists the chains that are in a given pdbfile
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

	print options.pdbfile + ": " + str(protein.numChains())
	for chain in protein.chain:
		print chain.name


	
if __name__ == "__main__":
	main()

