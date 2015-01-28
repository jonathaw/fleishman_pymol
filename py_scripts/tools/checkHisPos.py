#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Molecule import *
from Selection import *

def main():

	"""
WARNING: Not a generalized script
This script checks the relative orientations of a histidine and an asp (or glu).
When the protein is oriented along the Z-axis we expect the asp to be "above" the his.
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
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
	

	protein = Molecule()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		cat = getCatalyticResidues(protein)	

		his = None
		asp = None
		for c in cat:
			if c.name == "HIS":
				his = c
			if c.name == "GLU" or c.name == "ASP":
				asp = c

		if his == None or asp == None:
			print "cannot find catalytic residues"

		hnd = his.getAtom(" ND1")
		hne = his.getAtom(" NE2")
		
		if hnd.coord.z < hne.coord.z:
			hispos = hnd.coord.z
		else:
			hispos = hne.coord.z


		if asp.name == "ASP":
			asppos = asp.getAtom(" CG ").coord.z
		else:
			asppos = asp.getAtom(" CD ").coord.z
		
			
		if asppos < (hispos-0.5):
			print pdbfile,"FAIL"
		else:
			print pdbfile,"PASS"
		protein.clear()




if __name__ == "__main__":
	main()
