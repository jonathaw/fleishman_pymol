#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *


def main():

	"""
merges a list of pdbfiles into one large pdbfile (NMR format)
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="list", help="list")
	parser.add_option("-o", dest="output", help="output")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.list or not options.output:
		parser.print_help()
		sys.exit()

	try:
		PDBLIST = open(options.list)
	except:
		print "unable to open pdblist"
		sys.exit()

	try:
		OUTFILE = open(options.output, 'w')
	except:
		print "unable to open outfile"
		sys.exit()

	
	nModels = 0
	for pdbfile in PDBLIST.readlines():
		pdbfile = string.strip(pdbfile)
		nModels += 1

		try:
			PDBFILE = open(pdbfile)
		except:
			print "unable to open pdbfile", pdbfile

		OUTFILE.write("MODEL      %3i\n" % nModels)
		
		for line in PDBFILE.readlines():
			OUTFILE.write(line)	

		OUTFILE.write("ENDMDL\n")
		
	OUTFILE.close()



if __name__ == "__main__":
	main()
