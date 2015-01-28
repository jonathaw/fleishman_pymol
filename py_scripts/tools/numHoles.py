#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Enzyme import *
from Selection import *
from mol_routines import *
from file_routines import *


def main():

	"""
uses Will's packing 'holes' and reports the number of holes near a given selection
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-c", dest="catalytic", help="catalytic")
	parser.add_option("-x", dest="cutoff",  help="hole radius cuotoff", default="1.4")
	parser.add_option("-r", dest="radius",  help="radius around selection", default="4.0")
	parser.add_option("-v", dest="verbose", help="print holes", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()


	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	sele = Selection()
	if options.selection:
		sele.makeSelection(options.selection)

	hole_sele = Selection()
	hole_sele.makeSelection("resn=WSS")
	hole_radius = float(options.cutoff)


	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)

		holes = hole_sele.apply_selection(protein).atomList()
		if len(holes) == 0:
			print pdbfile,"no packing information found"
			protein.clear()
			continue

		catres = []
		if options.selection:
			protein = sele.apply_selection(protein)
		elif options.catalytic:
			if len(protein.catalytic) == 0:
				print "no catalytic information found!"
				sys.exit()
			catindex = int(options.catalytic)-1
			if catindex < 0 or catindex >= len(protein.catalytic):
				print "accessing catalytic residue out of bounds: ",catindex
				sys.exit()

			catres = protein.catalytic[catindex]

		if options.catalytic:
			protList = catres.atom
		else:
			protList = protein.atomList()

		surrounding = atomsAroundAtoms(atms=protList, atomList=holes, cutoff=float(options.radius))

		# filter based on radius of sphere
		outholes_b = []
		outholes   = []
		for atm in surrounding:
			if atm.bfactor > hole_radius:
				if not atm.occupancy in outholes_b:
					outholes.append(atm)
					outholes_b.append(atm.occupancy)

		print pdbfile,len(outholes)
		if options.verbose:
			for atm in outholes:
				print atm
			print "------------------------------------------------------"

		
		protein.clear()


if __name__ == "__main__":
	main()

