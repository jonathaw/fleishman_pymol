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
	prints the number of atoms that are near atoms in a given selection
	default does not include ligand atoms
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-c", dest="catalytic", help="catalytic sidechain")
	parser.add_option("-l", dest="ligand", help="ligand")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-S", dest="neighbor_selection", help="neighbor selection")
	parser.add_option("-x", dest="cutoff", help="distance cutoff (default 4.5)", default=4.5)
	parser.add_option("--include_ligand", dest="use_ligand", help="include ligand atoms", action="store_true")
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
	if options.neighbor_selection:
		sele2.makeSelection(options.neighbor_selection)

	if options.catalytic:
		cres = int(options.catalytic)
		cres -= 1

	cutoff = float(options.cutoff)
	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)

		atmlist = []
		alllist = []
		if options.catalytic:
			if cres >= len(protein.catalytic):
				print "accessing catalytic residue out of bounds"
				sys.exit()

			# just grab sidechain
			for mya in protein.catalytic[cres].atom:
				nm = mya.name
				if nm != " N  " and nm != " CA " and nm != " C  " and nm != " H  " and nm != " O  ":
					atmlist.append(mya)

		if options.selection:
			mol1 = sele1.apply_selection(protein)
			atmlist = mol1.atomList()

		if len(atmlist) == 0:
			print "selection does not specify any atoms"
			sys.exit()

		if options.neighbor_selection:
			mol2 = sele2.apply_selection(protein)
			alllist = mol2.atomList()
		else:
			if options.use_ligand:
				alllist = protein.atomList()
			else:
				alllist = protein.protein.atomList()

		taken = {}
		for atm in atmlist:
			for atm2 in alllist:
				if (atm2.resi == atm.resi):
					continue

				icb = int(atm2.file_id)
				if icb in taken.keys():
					continue

				dist = atm.distance(atm2)
				if dist < cutoff:
					taken[icb] = 1
				

		# subtract 1 from taken as it includes self
		print pdbfile,len(taken)-1
		protein.clear()
		



if __name__ == "__main__":
	main()
