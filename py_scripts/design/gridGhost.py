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
creates a ghost grid given a set of pdbfiles
	"""

	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="sele", help="sele")
	parser.add_option("-g", dest="grid", help="grid")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-c", dest="cutoff",  help="cutoff", default=3.0)
	(options, args) = parser.parse_args()

	if not options.pdblist or not options.grid:
		parser.print_help()
		sys.exit()

	if options.outfile:
		outgrid = options.outfile
	elif options.replace:
		outgrid = options.grid
	else:
		parser.print_help()
		sys.exit()

	if options.pdblist:
		try:
			PDBLIST = open(options.pdblist, 'r')
		except:
			print "unable to open pdblist"
			sys.exit()

		pdbfiles = []
		for line in PDBLIST.readlines():
			line = string.rstrip(line)
			pdbfiles.append(line)

	if options.sele:
		selection = Selection()
		selection.makeSelection(options.sele)

	mygrid = grid()		
	mygrid.read(options.grid)
	cloneGrid = grid()
	mygrid.clone(cloneGrid)
	mygrid.setUnoccupied()

	protein = Molecule()		
	for pdbfile in pdbfiles:
		print pdbfile
		protein.readPDB(pdbfile)


		if options.sele:
			newmol = selection.apply_selection(protein)
		else:
			newmol = protein.clone()

		atomlist = newmol.atomList()

		cloneGrid.setFullOccupied()
		gridTrimInclude(cloneGrid,atomlist,float(options.cutoff))
		mygrid.addGrid(cloneGrid)


		newmol.clear()
		protein.clear()

	npdb = len(pdbfiles)
	mygrid.intify(npdb)
	mygrid.write(outgrid)
		


if __name__ == "__main__":
	main()
