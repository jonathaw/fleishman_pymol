#!/usr/bin/python

import sys, string, commands
import random
from optparse import OptionParser
from Molecule import *
from Selection import *
from Fragment import *


def genFrags():
	"""
		
	This program will condense all fragments in a file into one position
	
	"""

	parser = OptionParser()
	parser.set_description(genFrags.__doc__)
	parser.add_option("-f", dest="fragfile", help="fragfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-n", dest="number", help="number", default=200)
	(options, args) = parser.parse_args()

	if not options.fragfile or not options.outfile:
		parser.print_help()
		sys.exit()

	lib = FragmentLibrary()
	lib.read(options.fragfile)
	npos = lib.numPositions()
	totfrags = int(options.number)
	frags_per_pos = (float(totfrags)/float(npos))

	fraglib = FragmentLibrary()
	fragpos = fraglib.newPosition()

	print "npos = ",npos

	frags_taken = 0
	for i in range(npos):
		if i == npos - 1:
			nleft = totfrags - frags_taken
		else:
			nleft = int(frags_per_pos*(i+1)) - frags_taken
		
		print i,nleft
		pos = lib.positions[i]
		fraglist = pos.getRandFragments(nleft)
		
		for frag in fraglist:
			fragpos.addFragment(frag)

		frags_taken += nleft

	fraglib.renumberPositions()
	fraglib.write(options.outfile)
		

if __name__ == "__main__":
	genFrags()

