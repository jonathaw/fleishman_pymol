#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from Molecule import *
from Builder import *

def main():

	"""
builds a new set of coords from three atoms in a pdbfile and a given distance, angle and torsion
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-i", dest="indices", help="atom indices (comma delimited)")
	parser.add_option("-v", dest="values", help="dist,ang,tor (comma delimited)")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.pdbfile:
		parser.print_help()
		sys.exit()

	if not options.indices or not options.values:
		parser.print_help()
		sys.exit()

	indices = options.indices.split(",")
	if len(indices) != 3:
		print "must supply 3 indices separated by a comma"
		sys.exit()

	values = options.values.split(",")
	if len(values) != 3:
		print "must supply 3 values separated by a comma"
		sys.exit()

	protein = Molecule()
	protein.readPDB(options.pdbfile)

	A = protein.getAtom(int(indices[0]))
	B = protein.getAtom(int(indices[1]))
	C = protein.getAtom(int(indices[2]))

	if A == None or B == None or C == None:
		print "cannot find all 3 atoms"
		sys.exit()

	length = float(values[0])
	ang = float(values[1])
	tor = float(values[2])

	billder = Builder()
	crd = billder.dbuildAtom(A, B, C, length, ang, tor)
	print '%8.3f%8.3f%8.3f' % (crd[0],crd[1],crd[2])



if __name__ == "__main__":
	main()
