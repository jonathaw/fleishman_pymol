#!/usr/bin/python

import sys, string, commands
from optparse import OptionParser
from Molecule import *
from Selection import *
from Fragment import *


def genFrags():
	"""
	
	This program extracts fragments from a fragment file
	
	"""

	parser = OptionParser()
	parser.set_description(genFrags.__doc__)
	parser.add_option("-f", dest="fragfile", help="fragfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-s", dest="selection", help="selection")
	(options, args) = parser.parse_args()

	if not options.fragfile or not options.outfile or not options.selection:
		parser.print_help()
		sys.exit()

	[beg,end] = options.selection.split("-")
	beg = int(beg)
	end = int(end)

	lib = FragmentLibrary()
	lib.read(options.fragfile)

	newlib = FragmentLibrary()
	for i in range(beg,end+1):
		pos = lib.getPosition(i)
		newlib.addPosition(pos)

	newlib.renumberPositions()
	newlib.write(options.outfile)
		

if __name__ == "__main__":
	genFrags()

