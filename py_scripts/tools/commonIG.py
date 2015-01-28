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
	parser.add_option("-t", dest="type1", help="type1")
	parser.add_option("-v", dest="set1", help="set1")
	parser.add_option("-x", dest="set2", help="set2")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file or not options.outfile:
		parser.print_help()
		sys.exit()
	
	IG = InteractionGraph()
	IG.read(options.file)
	IG.printStats()
	others = options.set1.split(",")
	iother1 = []
	for entry in others:
		iother1.append(num_from_aa1(entry))

	others = options.set2.split(",")
	iother2 = []
	for entry in others:
		iother2.append(num_from_aa1(entry))

	itype = num_from_aa1(options.type1)
	IG.commonInteraction(itype,iother1,iother2)
	IG.printStats()
	IG.write(options.outfile)

	


if __name__ == "__main__":
	main()
