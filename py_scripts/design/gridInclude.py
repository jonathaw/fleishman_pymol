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
modifies a grid to include a selection in a pdbfile or list of pdbfiles
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-g", dest="grid", help="grid")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-s", dest="selection", help="selection")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		try:
			LIST = open(options.pdblist, 'r')
		except:
			print "unable to open pdblist"
			sys.exit()

		for line in LIST.readlines():
			line = string.rstrip(line)
			pdbfiles.append(line)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	if not options.grid or not options.outfile:
		parser.print_help()
		sys.exit()

	try:
		OUTPUT = open(options.outfile, 'w')
	except:
		print "unable to create outfile"
		sys.exit()


	if options.selection:
		selection = Selection()
		selection.makeSelection(options.selection)

	protein = Molecule()		

	mygrid = grid()		
	mygrid.read(options.grid)

	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		if options.selection:
			newmol = selection.apply_selection(protein)
		else:
			newmol = protein.clone()


		atomlist = atomsInGrid(mygrid, newmol)
		OUTPUT.write(pdbfile + ": " + str(len(atomlist)) + "\n")
		print pdbfile,len(atomlist)

		protein.clear()
		newmol.clear()

	OUTPUT.close()


if __name__ == "__main__":
	main()
