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
maps the position of atoms in a pdbfile with an occupancy > 0 to a grid point
	"""

	parser = OptionParser()
	parser.add_option("-o", dest="outgrid", help="outgrid")
	parser.add_option("-i", dest="ingrid", help="ingrid")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.outgrid or not options.ingrid:
		parser.print_help()
		sys.exit()

	pdbfiles = []
	if options.pdblist:
		LIST = open(options.pdblist)
		for file in LIST.readlines():
			file = line.rstrip(file)
			pdbfiles.append(file)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	ingrid  = grid()
	outgrid = grid()

	ingrid.read(options.ingrid)
	ingrid.setUnoccupied()

	Protein = Molecule()
	for file in pdbfiles:
		Protein.readPDB(file)
		for chain in Protein.chain:
			for res in chain.residue:
				for atom in res.atom:
					if atom.occupancy > 0.0:
						zn = ingrid.getZone(atom=atom)
						ingrid.zone[zn[0]][zn[1]][zn[2]] = 1

		Protein.clear()
		
	ingrid.write(options.outgrid)
		


if __name__ == "__main__":
	main()
