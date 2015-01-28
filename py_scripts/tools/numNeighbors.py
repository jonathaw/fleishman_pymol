#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Enzyme import *
from Selection import *

def main():

	"""
	prints the number of CB's that are near atoms in a given selection
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-c", dest="catalytic", help="catalytic")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-x", dest="cutoff", help="distance cutoff", default=5.0)
	parser.add_option("-d", dest="directionality", help="directionality")
	parser.add_option("-S", dest="scaffold", help="scaffold")
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

	if not options.selection and not options.catalytic:
		parser.print_help()
		sys.exit()	

	sele1 = Selection()
	if options.selection:
		sele1.makeSelection(options.selection)

	sele2 = Selection()
	sele2.makeSelection("name= CA , CB ")

	if options.catalytic:
		cres = int(options.catalytic)
		cres -= 1

	if options.directionality:
		direction = float(options.directionality)

	
	scaffold = None
	if options.scaffold:
		scaffold = Molecule()
		scaffold.readPDB(options.scaffold)

	cutoff = float(options.cutoff)
	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)

		atmlist = []
		if options.catalytic:
			if cres >= len(protein.catalytic):
				print "accessing catalytic residue out of bounds"
				sys.exit()

			atmlist = protein.catalytic[cres].atom

		if options.selection:
			mol1 = sele1.apply_selection(protein)
			atmlist = mol1.atomList()

		if len(atmlist) == 0:
			print "selection does not specify any atoms"
			sys.exit()

		if options.scaffold:
			mol2 = sele2.apply_selection(scaffold)
		else:
			mol2 = sele2.apply_selection(protein)
		CBs = mol2.residueList()

		taken = {}
		if options.catalytic:
			com = protein.catalytic[cres].com()
		for atm in atmlist:
			for myres in CBs:
				cb = myres.getAtom(" CB ")
				if cb == None:
					continue

				icb = int(cb.file_id)
				if icb in taken.keys():
					continue

				dist = atm.distance(cb)
				if dist < cutoff:
					if options.directionality:
						if not isResPointingToPoint(myres, com, direction):
							continue
							
					taken[icb] = 1
				

		# subtract 1 from taken as it includes self
		print pdbfile,len(taken)-1
		protein.clear()
		



if __name__ == "__main__":
	main()
