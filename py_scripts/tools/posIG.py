#!/usr/bin/python

import string, sys
from optparse import OptionParser
from InteractionGraph import *
from pdb_routines import *

def main():

	"""
	restricts an interaction graph to given positions
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-l", dest="list", help="list")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-a", dest="aatype", help="aatype")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file or not options.outfile or not options.list:
		parser.print_help()
		sys.exit()

	if not options.aatype:
		parser.print_help()
		sys.exit()

	try:
		LIST = open(options.list)
	except:
		print "unable to open list"
		sys.exit()

	
	iaa = num_from_aa1(options.aatype)
	IG = InteractionGraph()
	IG.read(options.file)
	print "starting ..."
	IG.printStats()
         
	line = LIST.readline()
	pos = line.split()

	positions = []
	for i in pos:
		positions.append(int(i))
	
	IG.keepPositions(iaa, positions)
	IG.clean()
	print "ending ..."
	IG.printStats()
	IG.write(options.outfile)


if __name__ == "__main__":
	main()
