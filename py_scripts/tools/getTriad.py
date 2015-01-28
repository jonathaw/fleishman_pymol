#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from InteractionGraph import *
from pdb_routines import *

def main():

	"""
reports common interactions between two sets in an interaction graph
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-t", dest="triad", help="triad")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file or not options.outfile:
		parser.print_help()
		sys.exit()

	if not options.triad:
		parser.print_help()
		sys.exit()
	
	IG = InteractionGraph()
	IG.read(options.file)
	print "before:"
	IG.printStats()
	IG.getTriad(options.triad)
	print "after:"
	IG.printStats()
	IG.write(options.outfile)

	


if __name__ == "__main__":
	main()
