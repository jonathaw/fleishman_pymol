#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from Enzyme import *
from Builder import *
from file_routines import *
from Selection import *

def main():

	"""
solvates a histidine
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-c", dest="catalytic", help="catalytic")
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

	outfiles = []
	if options.outlist:
		outfiles = files_from_list(options.outlist)
	elif options.outfile:
		outfiles.append(options.outfile)
	elif options.replace:
		for file in pdbfiles:
			outfiles.append(file)
	else:
		parser.print_help()
		sys.exit()

	if len(outfiles) != len(pdbfiles):
		print "number of input and output files differ"
		sys.exit()

	if not options.catalytic:
		parser.print_help()
		sys.exit()

	icat = int(options.catalytic) - 1 
	protein = Enzyme()
	for i in range(len(pdbfiles)):
		protein.readPDB(pdbfiles[i])
		if icat < 0 or icat >= len(protein.catalytic):
			print "accessing catalytic residue out of bounds"
			sys.exit()

		cat = protein.catalytic[icat]
		if cat.name != "HIS":
			print "catalytic residue is not a histidine"
			sys.exit()

		# check protonation state
		if cat.getAtom(" HD1") != None:
			A = cat.getAtom(" NE2")
			B = cat.getAtom(" CD2")
			C = cat.getAtom(" CG ")
		elif cat.getAtom(" HE2") != None:
			A = cat.getAtom(" ND1")
			B = cat.getAtom(" CE1")
			C = cat.getAtom(" NE2")
		else:
			print "unable to determine protonation state"
			sys.exit()

		if A == None or B == None or C == None:
			print "cannot find all 3 atoms"
			sys.exit()

		length = 2.98
		ang    = 125.0
		tor    = 180.0

		billder = Builder()
		crd = billder.dbuildAtom(A, B, C, length, ang, tor)
		newres = protein.chain[1].newResidue()
		newres.name = "LG2"

		newatm = newres.newAtom()
		newatm.coord.x = crd[0]
		newatm.coord.y = crd[1]
		newatm.coord.z = crd[2]
		newatm.name    = "HOH "
		newatm.kind    = "HETATM"
		
		protein.writePDB(outfiles[i])
		protein.clear()





if __name__ == "__main__":
	main()
