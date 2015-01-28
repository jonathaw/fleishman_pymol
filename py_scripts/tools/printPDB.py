#!/usr/bin/python

from optparse import OptionParser
import sys, string
from Molecule import *
from Selection import *


def main():

	"""
	program that prints out selections from a pdbfile
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-s", dest="selection", help="selection")
	(options, args) = parser.parse_args()

	if not options.pdbfile or not options.selection:
		parser.print_help()
		sys.exit()

	protein = Molecule()
	protein.readPDB(options.pdbfile)
	
	sele = Selection()
	sele.makeSelection(options.selection)
	smol = sele.apply_selection(protein)
	reslist = smol.residueList()

	for res in reslist:
		print res



if __name__ == "__main__":
	main()

