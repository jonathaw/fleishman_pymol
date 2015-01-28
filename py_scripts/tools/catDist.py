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
reports the distance of two atoms.  One of these atoms must be catalytic and 
designation by its residue number (-c) and name (-n)
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-c", dest="catalytic", help="catalytic residue")
	parser.add_option("-n", dest="catname", help="catalytic name")
	parser.add_option("--s1", dest="selection1", help="selection1")
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

	if not options.selection1:
		parser.print_help()
		sys.exit()	

	if not options.catalytic or not options.catname:
		parser.print_help()
		sys.exit()

	sele1 = Selection()
	sele1.makeSelection(options.selection1)

	cres = int(options.catalytic)
	cres -= 1

	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)

		if cres > len(protein.catalytic):
			print "accessing catalytic residue out of bounds"
			sys.exit()

		mol1 = sele1.apply_selection(protein)

		catres = protein.catalytic[cres]
		catatom = catres.getAtom(options.catname)
		if catatom == None:
			protein.clear()
			continue

		alist1 = mol1.atomList()

		if len(alist1) != 1:
			print "selection 1 does not specify 1 atom"
			sys.exit()

		atm1 = alist1[0]
		dist = atm1.distance(catatom)
		print pdbfile,":",atm1.name,"->",catatom.name,":",dist
		protein.clear()
		



if __name__ == "__main__":
	main()
