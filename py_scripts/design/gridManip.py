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
provides basic grid manipulation abilites such as movement of occupancy functions
	"""

	parser = OptionParser()
	parser.add_option("-g", "--grid", dest="grid", help="grid")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-c", dest="center",  help="center")
	parser.add_option("-t", dest="translate", help="translate")
	parser.add_option("-f", dest="fill", help="fill", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.grid:
		parser.print_help()
		sys.exit()

	if options.outfile:
		outgrid = options.outfile
	elif options.replace:
		outgrid = options.grid
	else:
		parser.print_help()
		sys.exit()


	mygrid = grid()		
	mygrid.read(options.grid)

	if options.center:
		cols = options.center.split(",")
		mygrid.center(int(cols[0]), int(cols[1]), int(cols[2]))
	if options.translate:
		cols = options.center.split(",")
		mygrid.translate(int(cols[0]), int(cols[1]), int(cols[2]))
	if options.fill:
		mygrid.setFullOccupied()
	
	mygrid.write(outgrid)
		


if __name__ == "__main__":
	main()
