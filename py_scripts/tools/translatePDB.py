#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *


def main():

	"""
	translates a molecule by a given x,y,z vector
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-v", dest="vector",  help="vector")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()


	if not options.pdbfile:
		parser.print_help()
		sys.exit()

	if options.outfile:
		output = options.outfile
	elif options.replace:
		output = options.pdbfile
	else:
		parser.print_help()
		sys.exit()

	if not options.vector:
		parser.print_help()
		sys.exit()

	(x,y,z) = options.vector.split(",")
	myvec = vector3d(float(x), float(y), float(z))

	mymol = Molecule()
	mymol.readPDB(options.pdbfile)
	mymol.translate(myvec)
	mymol.writePDB(output, resRenumber=False, atomRenumber=False)



if __name__ == "__main__":
	main()

