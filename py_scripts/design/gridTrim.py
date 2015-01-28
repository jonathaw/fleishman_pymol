#!/usr/bin/python

Author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import os, sys, string, commands
from optparse import OptionParser
from mol_routines import *
from grid_functions import *
from Molecule import *
from Selection import *


def main():

	"""
trims a grid for a given selection and cutoff values
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-s", dest="sele", help="sele")
	parser.add_option("-g", dest="grid", help="grid")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-e", dest="exclude", help="exclude", action="store_true")
	parser.add_option("-c", dest="cutoff",  help="cutoff", default=3.0)
	(options, args) = parser.parse_args()

	if not options.pdbfile or not options.grid:
		parser.print_help()
		sys.exit()

	if options.outfile:
		outgrid = options.outfile
	elif options.replace:
		outgrid = options.grid
	else:
		parser.print_help()
		sys.exit()

	protein = Molecule()		
	protein.readPDB(options.pdbfile)

	if options.sele:
		selection = Selection()
		selection.makeSelection(options.sele)
		newmol = selection.apply_selection(protein)
	else:
		newmol = protein.clone()


	mygrid = grid()		
	mygrid.read(options.grid)

	atomlist = newmol.atomList()
	if options.exclude:
		gridTrimExclude(mygrid,atomlist,float(options.cutoff))
	else:
		gridTrimInclude(mygrid,atomlist,float(options.cutoff))

	mygrid.write(outgrid)
		


if __name__ == "__main__":
	main()
