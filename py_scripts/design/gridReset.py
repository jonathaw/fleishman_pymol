#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import os, sys, string, commands
from optparse import OptionParser
from mol_routines import *
from grid_functions import *
from Molecule import *
from Selection import *



def main():

	"""
resets the boundaries of a given grid
	"""

	parser = OptionParser()
	parser.add_option("-i", dest="ingrid", help="ingrid")
	parser.add_option("-o", dest="outgrid", help="outgrid")
	(options, args) = parser.parse_args()

	if not options.ingrid or not options.outgrid:
		parser.print_help()
		sys.exit()

	mygrid = grid()		
	mygrid.read(options.ingrid)
	gridReset(mygrid)
	mygrid.write(options.outgrid)


if __name__ == "__main__":
	main()
