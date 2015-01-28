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
checks the angle of a pi-stacking residue (PHE,TYR, or TRP) with the ligand
(3 specified atoms in a plane)
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-c", dest="catalytic", help="catalytic")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-x", dest="cutoff", help="cutoff")
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true")
	parser.add_option("-v", dest="verbose", help="verbose", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.catalytic or not options.selection:
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
	

	protein = Enzyme()
	icat = int(options.catalytic) - 1
	sele = Selection()
	sele.makeSelection(options.selection)
	
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		cres = protein.catalytic[icat]
		#cres = getCatalyticResidue(protein, icat)	
		if cres == None:
			print "cannot find catalytic residue"
			sys.exit()

		alist = sele.apply_selection(protein).atomList()
		if len(alist) != 3:
			print "invalid selection"
			for atm in alist:
				print atm
			sys.exit()

		# --- get the normal of the ligand--- #
		AB = alist[0].coord - alist[1].coord
		BC = alist[2].coord - alist[1].coord
		ligvec = AB.cross(BC)

		# --- get the normal of the catres --- #
		if cres.name == "PHE" or cres.name == "TYR" or cres.name == "TRP":
			A = cres.getAtom(" CD1")
			B = cres.getAtom(" CG ")
			C = cres.getAtom(" CD2")
		else:
			if options.verbose:
				print "invalid catalytic residue:",cres.name
				print pdbfile, "N/A"

			protein.clear()
			continue
			#sys.exit()

		AB = A.coord - B.coord
		BC = C.coord - B.coord
		catvec = AB.cross(BC)

		ang = ligvec.angle(catvec)
		if ang > 90:
			ang = 180 - ang

		if options.cutoff:
			if options.inverse:
				if ang > float(options.cutoff):
					print pdbfile,ang
			else:
				if ang < float(options.cutoff):
					print pdbfile,ang
		else:
			print pdbfile,ang
		
		protein.clear()




if __name__ == "__main__":
	main()
