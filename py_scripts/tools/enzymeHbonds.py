#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Enzyme import *
from Hbond import *

def main():

	"""
reports the hydrogen bonds made to catalytic residues in an enzyme
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-c", dest="catalytic", help="catalytic")
	parser.add_option("-x", dest="cutoff", help="cutoff", default=-0.3)
	parser.add_option("-m", dest="mabo", help="mabo", action="store_true")
	parser.add_option("-n", dest="count", help="report counts", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.catalytic:
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
	
	enz  = Enzyme()
	icat = int(options.catalytic)

	HBN = HBnetwork()
	
	for pdbfile in pdbfiles:
		enz.readPDB(pdbfile)
		cres = enz.catalytic[icat-1]
		if cres == None:
			print "cannot find catalytic residue"
			sys.exit()

		HBN.createNetwork(enz)
		HBN.findHbonds(float(options.cutoff))
		hlist = HBN.getHbondsToResidue(cres)

		if options.count:
			print pdbfile,len(hlist)
		else:
			for hb in hlist:
				print pdbfile,hb

		HBN.clear()
		enz.clear()




if __name__ == "__main__":
	main()
