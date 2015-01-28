#!/usr/bin/python

import sys, os, string
from optparse import OptionParser
from Molecule import *
from Builder import *
from Selection import *

def main():

	"""
builds new atoms onto existing pdbfiles.  EXPERIMENTAL AND UNTESTED
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("--dist", dest="distance", help="distance")
	parser.add_option("--ang", dest="angle", help="angle")
	parser.add_option("--tor", dest="torsion", help="torsion")
	parser.add_option("-s","--selection", dest="selection", help="selection")
	parser.add_option("-b", "--build", dest="build", help="build")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.pdbfile or not options.selection:
		parser.print_help()
		sys.exit()

	if not options.outfile:
		parser.print_help()
		sys.exit()

	mol = Molecule()
	mol.readPDB(options.pdbfile)

	selector = Selection()
	selector.makeSelection(options.selection)
	mysel = selector.apply_selection(mol)

	builder = Builder()

	atomlist = mysel.atomList()
	if len(atomlist) != 3:
		print "must select three atoms. ",len(atomlist)

	newatom = Atom()
	newatom.name = "new"
	dist = float(options.distance)
	ang  = float(options.angle)
	tor  = float(options.torsion)
	builder.buildAtom(newatom, atomlist[0], atomlist[1], atomlist[2],
		dist, ang, tor)

	mol.chain[0].residue[0].addAtom(newatom)
	mol.writePDB(options.outfile)
		
	

if __name__ == "__main__":
	main()
