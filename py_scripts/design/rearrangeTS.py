#!/usr/bin/python


import os, sys, string, commands
from optparse import OptionParser
from transition_state import *

def main():
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	(options, args) = parser.parse_args()

	if not options.pdbfile or not options.outfile:
		parser.print_help()
		sys.exit()

	TS = transition_state()
	TS.read(options.pdbfile)
	TS.arrange()
	TS.write(options.outfile)
				



if __name__ == "__main__":
	main()
