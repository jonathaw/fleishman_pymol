#!/usr/bin/python

import string, sys
from optparse import OptionParser
from InteractionGraph import *
from pdb_routines import *

def main():

	"""
	combines two interaction graphs
	"""

	parser = OptionParser()
	parser.add_option("--file1", dest="file1", help="file1")
	parser.add_option("--file2", dest="file2", help="file2")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file1 or not options.file2:
		parser.print_help()
		sys.exit()

	if not options.outfile:
		parser.print_help()
		sys.exit()
	
	IG1 = InteractionGraph()
	IG1.read(options.file1)
	print "IG1:"
	IG1.printStats()

	print ""
	IG2 = InteractionGraph()
	IG2.read(options.file2)
	print "IG2:"
	IG2.printStats()

	print ""
	IG1.combineIG(IG2)
	print "after:"
	IG1.printStats()
	
	IG1.clean()
	print "ending ..."
	IG1.write(options.outfile)


if __name__ == "__main__":
	main()
