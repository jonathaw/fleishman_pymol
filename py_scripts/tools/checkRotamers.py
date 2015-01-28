#!/usr/bin/python

import string, sys
from optparse import OptionParser
from RotamerSet import *


def main():

	"""
checks to see which rotamers are not within 1 stdev of the bbdep values
takes a torsion file input (run torsion.pl first)
	"""

	parser = OptionParser()
	parser.add_option("-t", dest="torsion", help="torsion")
	parser.add_option("-d", dest="dunbrack", help="dunbrack")
	parser.add_option("-s", dest="stdev", help="stdev", default=1.0)
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.torsion or not options.dunbrack or not options.outfile:
		parser.print_help()
		sys.exit()

	try:
		TORSION = open(options.torsion)
	except:
		print "unable to open torsions file"
		sys.exit()

	try:
		OUTPUT = open(options.outfile, 'w')
	except:
		print "unable to open output file"
		sys.exit()

	lib = RotamerLibrary()
	lib.setStdev(float(options.stdev))
	lib.read(options.dunbrack)

	for line in TORSION:
		line = string.rstrip(line)

		cols = line.split()	
		pos  = int(cols[1])
		aa3  = cols[2]
		phi  = float(cols[3])
		psi  = float(cols[4])
		ome  = float(cols[5])
		chi1 = float(cols[6]) + 180.0
		chi2 = float(cols[7]) + 180.0
		chi3 = float(cols[8]) + 180.0
		chi4 = float(cols[9]) + 180.0

		if not lib.allowed(aa3,phi,psi,chi1,chi2,chi3,chi4):
			OUTPUT.write(str(pos) + " " + aa3 + "\n")

	OUTPUT.close()


if __name__ == "__main__":
	main()
