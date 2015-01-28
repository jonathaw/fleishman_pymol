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
reports the distance between two selected atoms in a pdbfile
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("--s1", dest="selection1", help="selection1")
	parser.add_option("--s2", dest="selection2", help="selection2")
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

	if not options.selection1 or not options.selection2:
		parser.print_help()
		sys.exit()	

	sele1 = Selection()
	sele2 = Selection()
	sele1.makeSelection(options.selection1)
	sele2.makeSelection(options.selection2)

	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		mol1 = sele1.apply_selection(protein)
		mol2 = sele2.apply_selection(protein)
	
		alist1 = mol1.atomList()
		alist2 = mol2.atomList()

		if len(alist1) != 1:
			print "selection 1 does not specify 1 atom"
			print alist1
			sys.exit()

		if len(alist2) != 1:
			print "selection 2 does not specify 1 atom"
			sys.exit()

		atm1 = alist1[0]
		atm2 = alist2[0]

		dist = atm1.distance(atm2)
		print pdbfile,":",atm1.name,"->",atm2.name,":",dist
		protein.clear()
		



if __name__ == "__main__":
	main()
