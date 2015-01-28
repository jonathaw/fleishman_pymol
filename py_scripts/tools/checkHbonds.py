#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from file_routines import *
from Molecule import *
from Selection import *
from Hbond import *

def main():

	"""
list the hydrogen bonds in a protein that have a score less than a given threshold
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-S", dest="summary", help="summary", action="store_true")
	parser.add_option("-x", dest="cutoff", help="cutoff", default=-0.3)
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

	sele = Selection()
	if options.selection:
		sele.makeSelection(options.selection)
		

	protein = Enzyme()
	HBN = HBnetwork()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		newprot = protein
		if options.selection:
			newprot = sele.apply_selection(protein)

		HBN.createNetwork(newprot)
		HBN.findHbonds(cutoff=float(options.cutoff))

		found = False
		if options.summary:
			print pdbfile,len(HBN.hbonds)
			found = True
		else:
			for hb in HBN.hbonds:
				print pdbfile,hb
				found = True

		if not found:
			print pdbfile,"NONE"

		protein.clear()
		HBN.clear()




if __name__ == "__main__":
	main()
