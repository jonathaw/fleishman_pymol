#!/usr/bin/python

import sys
from optparse import OptionParser
from Molecule import *
from file_routines import *


def main():

	"""
creates a fasta file from a given pdbfile
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdblist = []
	if options.pdblist:
		pdblist = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdblist.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()


	protein = Molecule()
	for pdbfile in pdblist:
		protein.readPDB(pdbfile)
		seq = protein.sequence()
		protein.clear()

		print ">"+pdbfile+" 1-"+str(len(seq))

	#	if "x" in seq:
	#		print "protein contains hetero atoms"
			#sys.exit()


		lenline = 50
		nseq   = len(seq)
		nlines = nseq/lenline + 1
		start = 0
		end   = lenline
		for i in range(nlines):
			out = seq[start:end]
			start += lenline
			end += lenline
			print out




if __name__ == "__main__":
	main()
