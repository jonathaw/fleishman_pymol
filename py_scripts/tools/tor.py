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
reports the angle between three uniquely identified atoms in a pdbfile
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("--s1", dest="selection1", help="selection1")
	parser.add_option("--s2", dest="selection2", help="selection2")
	parser.add_option("--s3", dest="selection3", help="selection3")
	parser.add_option("--s4", dest="selection4", help="selection4")
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
	sele3 = Selection()
	sele4 = Selection()
	sele1.makeSelection(options.selection1)
	sele2.makeSelection(options.selection2)
	sele3.makeSelection(options.selection3)
	sele4.makeSelection(options.selection4)

	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		mol1 = sele1.apply_selection(protein)
		mol2 = sele2.apply_selection(protein)
		mol3 = sele3.apply_selection(protein)
		mol4 = sele4.apply_selection(protein)
	
		alist1 = mol1.atomList()
		alist2 = mol2.atomList()
		alist3 = mol3.atomList()
		alist4 = mol4.atomList()

		if len(alist1) != 1:
			print "selection 1 does not specify 1 atom"
			sys.exit()

		if len(alist2) != 1:
			print "selection 2 does not specify 1 atom"
			sys.exit()

		if len(alist3) != 1:
			print "selection 3 does not specify 1 atom"
			sys.exit()

		if len(alist4) != 1:
			print "selection 4 does not specify 1 atom"
			sys.exit()
		
		atm1 = alist1[0]
		atm2 = alist2[0]
		atm3 = alist3[0]
		atm4 = alist4[0]

		tor = vector3d.torsion(atm1.coord, atm2.coord, atm3.coord, atm4.coord)
		print pdbfile,":",atm1.name,"->",atm2.name,"->",atm3.name,"->",atm4.name,":",tor
		protein.clear()
		



if __name__ == "__main__":
	main()
