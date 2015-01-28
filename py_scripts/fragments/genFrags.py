#!/usr/bin/python

import sys, string, commands
from optparse import OptionParser
from Molecule import *
from Selection import *


def genFrags():
	"""This program generates fragment files for a given protein. """

	parser = OptionParser()
	parser.set_description(genFrags.__doc__)
	parser.set_usage("-p pdbfile -s selection")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-s", dest="selection", help="selection")
	(options, args) = parser.parse_args()

	if not options.pdbfile:
		parser.print_help()
		sys.exit()



if __name__ == "__main__":
	genFrags()

