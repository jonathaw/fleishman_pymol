#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import os, sys, string, commands
from optparse import OptionParser
from grid_functions import *



def main():

	"""
creates a new grid of given dimensions
	"""

	parser = OptionParser()
	parser.add_option("-g", dest="gridfile", help="new grid file")
	parser.add_option("-x", dest="num_x", help="nX")
	parser.add_option("-y", dest="num_y", help="nY")
	parser.add_option("-z", dest="num_z", help="nZ")
	parser.add_option("-n", dest="num",   help="num grid points (cubic)")
	parser.add_option("-l", dest="length", help="length", default=1.0)
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.gridfile:
		parser.print_help()
		sys.exit()

	nX = 0
	nY = 0
	nZ = 0
	if options.num:
		nX = int(options.num)
		nY = int(options.num)
		nZ = int(options.num)
	elif options.num_x and options.num_y and options.num_z:
		nX = int(options.num_x)
		nY = int(options.num_y)
		nZ = int(options.num_z)
	else:
		parser.print_help()
		sys.exit()
		
	mygrid = grid(nX=nX, nY=nY, nZ=nZ, length=float(options.length))
	mygrid.write(options.gridfile)



if __name__ == "__main__":
	main()
