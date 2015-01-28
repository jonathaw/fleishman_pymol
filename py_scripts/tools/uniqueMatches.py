#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Enzyme import *

def main():

	"""
reports a list of unique matches.  This is defined by the identity of the 
catalytic residues and the position of space of the ligand (discreteness defined
by the "fineness" option)
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-f", dest="fineness", help="fineness (0.25)", default=0.25)
	parser.add_option("-s", dest="seq_only", help="sequence only", action="store_true")
	parser.add_option("--heavy_atom_only", dest="heavy_only", help="only heavy atoms considered", action="store_true")
	parser.add_option("-r", dest="report", help="report unique matches only", action="store_true")
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true")
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

	protein = Enzyme()
	fineness = float(options.fineness)
	seen = {}
	for pdbfile in pdbfiles:
		name = ""
		protein.readPDB(pdbfile)
		com = vector3d()
		if options.heavy_only:
			natom = 0
			for atm in protein.chain[0].atomList():
				if atm.element != "H":
					com.x += atm.coord.x
					com.y += atm.coord.y
					com.z += atm.coord.z
					natom += 1

			if natom > 0:
				com /= float(natom)
		else:
			com = protein.chain[0].com()

		lcom = protein.ligand.com()
		# get absolute value of ligand coordinates
		rcom = vector3d()
		nat = 0
		for atm in protein.ligand.atom:
			rcom.x += math.fabs(atm.coord.x-lcom.x)
			rcom.y += math.fabs(atm.coord.y-lcom.y)
			rcom.z += math.fabs(atm.coord.z-lcom.z)
			nat += 1

		if nat == 0:
			print "no ligand atoms founds"
			sys.exit()

			
		for cat in protein.catalytic:
			name += cat.aa1() + str(int(cat.file_id)) + "_"

		# get the ligand position
		if not options.seq_only:
			lpoint = (lcom - com)/fineness
			rcom /= fineness
			name += str(int(lpoint.x)) + "_"
			name += str(int(lpoint.y)) + "_"
			name += str(int(lpoint.z)) + "_"
			name += str(int(rcom.x)) + "_"
			name += str(int(rcom.y)) + "_"
			name += str(int(rcom.z))

		if options.report:
			if options.inverse:
				if name in seen.keys():
					print pdbfile,name
			else:
				if not (name in seen.keys()):
					print pdbfile,name
		else:
			print pdbfile,name

		seen[name] = 1

		protein.clear()
		



if __name__ == "__main__":
	main()
