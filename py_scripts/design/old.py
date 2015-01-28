#!/usr/bin/python


import os, sys, string, commands
from optparse import OptionParser

def main():
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-s", dest="sort", help="sort", action="store_true")
	parser.add_option("-b", dest="bvalue", help="b value")
	parser.add_option("-i", dest="increment", help="increment", action="store_true")
	(options, args) = parser.parse_args()

	if not options.pdbfile:
		parser.print_help()
		sys.exit()
	
	outfile = ""
	if options.outfile:
		outfile = options.outfile
	elif options.replace:
		outfile = options.pdbfile
	else:
		parser.print_help()
		sys.exit()


	TS = transition_state()
	TS.read(options.pdbfile)
	
	b = 0.0
	for atom in TS.atom:
		if options.bvalue:
			atom.b = float(options.bvalue)
		elif options.increment:
			b += 1.0
			atom.b = b

	TS.write(outfile)	
			


if __name__ == "__main__":
	main()
