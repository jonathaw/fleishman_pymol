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
reports the scores for a catalytic residue
format: Erep,Eatr,Esol,EhbBB,EhbSC
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-c", dest="catalytic", help="catalytic residue")
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

	if not options.catalytic:
		parser.print_help()
		sys.exit()

	cres = int(options.catalytic)
	cres -= 1

	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)

		if cres > len(protein.catalytic):
			print "accessing catalytic residue out of bounds"
			sys.exit()

		catres = protein.catalytic[cres]
		print pdbfile,catres.name,catres.Erep,catres.Eatr,catres.Esol,catres.EhbBB,catres.EhbSC
		protein.clear()
		



if __name__ == "__main__":
	main()
