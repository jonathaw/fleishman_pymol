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
fluffs a grid by a given number of cells - expands the number of occurpied cells
	"""

	parser = OptionParser()
	parser.add_option("-g", dest="original", help="original")
	parser.add_option("-o", dest="outgrid", help="outgrid")
	parser.add_option("-i", dest="ingrid", help="ingrid")
	parser.add_option("-n", dest="number", help="number", default=4)
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.original or not options.outgrid or not options.ingrid:
		parser.print_help()
		sys.exit()

	origrid = grid()
	ingrid  = grid()
	outgrid = grid()

	origrid.read(options.original)
	ingrid.read(options.ingrid)

	if not origrid.equalDimensions(ingrid):
		print "grids must have equal dimensions"
		sys.exit()

	outgrid.name = ingrid.name

	mynum = int(options.number)
	ingrid.clone(outgrid)
	for i in range(ingrid.nX+1):
		for j in range(ingrid.nY+1):
			for k in range(ingrid.nZ+1):
				if ingrid.zone[i][j][k] != 0:

					istart = max(0, (i - mynum))
					iend   = min(ingrid.nX+1, (i + mynum))

					jstart = max(0, (j - mynum))
					jend   = min(ingrid.nY+1, (j + mynum))

					kstart = max(0, (k - mynum))
					kend   = min(ingrid.nZ+1, (k + mynum))

					for ii in range(istart,iend):
						for jj in range(jstart,jend):
							for kk in range(kstart, kend):
							   if origrid.zone[ii][jj][kk] != 0:
									outgrid.zone[ii][jj][kk] = 1
	
	outgrid.write(options.outgrid)
		


if __name__ == "__main__":
	main()
