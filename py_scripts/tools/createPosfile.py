#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *

def main():

	"""
	creates a posfile from a protein
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.pdbfile or not options.outfile:
		parser.print_help()
		sys.exit()

	try:
		OUTFILE = open(options.outfile, 'w')
	except:
		print "unable to create posfile"
		sys.exit()

	mol = Molecule()
	mol.readPDB(options.pdbfile)
	nres = mol.numResidues()
	for i in range(1,nres+1):
		OUTFILE.write(str(i)+" ")
	OUTFILE.close()
	mol.clear()
	


if __name__ == "__main__":
	main()
