#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import os, sys, string, commands
from optparse import OptionParser
from grid_functions import *



def main():

	"""
expands a given grid by a given number of grid points in all directions
	"""

	parser = OptionParser()
	parser.add_option("-g", dest="gridfile", help="input grid file")
	parser.add_option("-o", dest="outfile", help="output grid file")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-n", dest="num",   help="number of expansion")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.gridfile or not options.num:
		parser.print_help()
		sys.exit()

	outfile = ""
	if options.outfile:
		outfile = options.outfile
	elif options.replace:
		outfile = options.gridfile
	else:
		parser.print_help()
		sys.exit()

	expansion = float(options.num)
	mygrid = grid()
	mygrid.read(options.gridfile)

	mygrid.base.x -= mygrid.length*expansion
	mygrid.base.y -= mygrid.length*expansion
	mygrid.base.z -= mygrid.length*expansion

	mygrid.nX += 2*int(options.num)
	mygrid.nY += 2*int(options.num)
	mygrid.nZ += 2*int(options.num)

	mygrid.setupZones()
	mygrid.setFullOccupied()
	
	mygrid.write(outfile)



if __name__ == "__main__":
	main()
