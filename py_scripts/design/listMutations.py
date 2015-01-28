#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from file_routines import *
from Enzyme import *

def main():

	"""
	prints a list of mutations between a designed sequence and a native sequence
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-n", dest="native", help="native")
	parser.add_option("-t", dest="type", help="type")
	parser.add_option("-T", dest="origType", help="original type")
	parser.add_option("-s", dest="summary", help="print pdbfile only", action="store_true")
	parser.add_option("-c", dest="count", help="count", action="store_true")
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

	if not options.native:
		parser.print_help()
		sys.exit()
	

	native = Enzyme()
	native.readPDB(options.native)
	protein = Enzyme()

	natseq = native.sequence()
	for pdbfile in pdbfiles:
		nmut = 0
		mut_found = False
		protein.readPDB(pdbfile)
		mutseq = protein.sequence()

		mysize = min(len(natseq), len(mutseq))
		for i in range(mysize):
			if natseq[i] != mutseq[i]:
				if options.type:
					if not (mutseq[i] in options.type):
						continue
				if options.origType:
					if not (natseq[i] in options.origType):
						continue

				mut_found = True
				nmut += 1
				if not options.summary:
					print i+1,natseq[i],"->",mutseq[i]

		if options.summary and mut_found:
			if options.count:
				print pdbfile,nmut
			else:
				print pdbfile

		protein.clear()

	native.clear()
		



if __name__ == "__main__":
	main()

