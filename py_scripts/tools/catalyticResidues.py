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
prints the list of catalytic residues in the enzme. (name and position)
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

	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		seq = ""
		pos = ""

		for cat in protein.catalytic:
			seq += cat.name + "-"

		for cat in protein.catalytic:
			pos += cat.file_id + " "

		print pdbfile,seq,pos
		protein.clear()
		



if __name__ == "__main__":
	main()
