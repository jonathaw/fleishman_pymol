#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Molecule import *

def main():

	"""
	checks the angle of a pi-stacking residue with the ligand
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("--c1", dest="catalytic1", help="catalytic1")
	parser.add_option("--c2", dest="catalytic2", help="catalytic2")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.catalytic1 or not options.catalytic2:
		parser.print_help()
		sys.exit()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()
	

	protein = Molecule()
	icat1 = int(options.catalytic1)
	icat2 = int(options.catalytic2)
	
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		cres1 = getCatalyticResidue(protein, icat1)
		cres2 = getCatalyticResidue(protein, icat2)
		if cres1 == None or cres2 == None:
			print "cannot find catalytic residue"
			sys.exit()

		if cres1.name == "HIS":
			his = cres1
			asp = cres2
		elif cres2.name == "HIS":
			his = cres2
			asp = cres1
		
		A = his.getAtom(" 
		
		ang = ligvec.angle(catvec)
		if ang > 90:
			ang = 180 - ang
		print pdbfile,ang
		
		protein.clear()




if __name__ == "__main__":
	main()
