#!/usr/bin/python

import sys, string, commands
import random
from optparse import OptionParser
from Molecule import *
from Selection import *
from Fragment import *


def genFrags():
	"""
		
	This program will merge fragment files to generate one fragment file
	
	"""

	parser = OptionParser()
	parser.set_description(genFrags.__doc__)
	parser.add_option("-F", dest="fraglist", help="fraglist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-n", dest="number", help="number", default=200)
	(options, args) = parser.parse_args()

	if not options.fraglist or not options.outfile:
		parser.print_help()
		sys.exit()

	try:
		FRAGLIST = open(options.fraglist, 'r')
	except:
		print "unable to open fragment list"
		sys.exit()

	fragfiles = []
	for line in FRAGLIST.readlines():
		line = string.rstip(line)
		fragfiles.append(fragfiles)

	FRAGLIST.close()

	lib = FragmentLibrary()
	totfrags = options.number

	fraglib = FragmentLibrary()
	fragpos = fraglib.newPosition()
	for fragfile in fragfiles:
		fraglib.read(fragfile)
			
		fraglib.clear()


	newlib = FragmentLibrary()
	for i in range(beg,end+1):
		pos = lib.getPosition(i)
		newlib.addPosition(pos)

	newlib.renumberPositions()
	newlib.write(options.outfile)
		

if __name__ == "__main__":
	genFrags()

