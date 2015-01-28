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
checks the hydrogen bond between residues in a backed up match
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("--c1", dest="catalytic1", help="catalytic1")
	parser.add_option("--c2", dest="catalytic2", help="catalytic2")
	parser.add_option("-c", dest="cutoff", help="cutoff", default=-0.3)
	parser.add_option("-m", dest="mabo", help="mabo", action="store_true")
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
	

	protein = Enzyme()
	icat1 = int(options.catalytic1) - 1
	icat2 = int(options.catalytic2) - 1

	HBN = HBnetwork()
	
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		#cres1 = getCatalyticResidue(protein, icat1)
		#cres2 = getCatalyticResidue(protein, icat2)
		cres1 = protein.catalytic[icat1]
		cres2 = protein.catalytic[icat2]
		if cres1 == None or cres2 == None:
			print "cannot find catalytic residue"
			sys.exit()

		clist = []
		clist.append(cres1)
		clist.append(cres2)

		HBN.createNetwork(reslist=clist)
		HBN.findHbonds(float(options.cutoff))

		if HBN.numHbonds() < 1:
			print pdbfile,"none"
		else:
			for hb in HBN.hbonds:
				print pdbfile,hb.energy

		HBN.clear()
		protein.clear()




if __name__ == "__main__":
	main()
