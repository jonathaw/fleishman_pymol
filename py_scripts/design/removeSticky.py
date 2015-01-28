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
reads a rosetta output pdbfile and reports residues that have a total Eres  > cutoff
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-t", dest="type",    help="atom type", default="CS1 ")
	parser.add_option("-T", dest="type2",   help="atom type", default="CS2 ")
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

	if len(pdbfiles) != len(outfiles):
		print "number of pdbfiles and output files differ"
		sys.exit()

	mymol = Enzyme()
	for i in range(len(pdbfiles)):
		pdbfile = pdbfiles[i]
		outfile = outfiles[i]
		mymol.readPDB(pdbfile)

		lig = mymol.ligand
		lig.removeAtomsContaining(options.type)
		lig.removeAtomsContaining(options.type2)
			
		mymol.writePDB(outfile)
		mymol.clear()


if __name__ == "__main__":
	main()
