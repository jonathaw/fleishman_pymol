#!/usr/bin/python

"""
	analyzes stuff
"""

import os, sys, string, commands, re
from optparse import OptionParser
from Molecule import *

def main():
	parser = OptionParser()
	parser.add_option("-f", dest="binfile", help="binfile")
	parser.add_option("-b", dest="bin", help="bin", default=0.5)
	parser.add_option("-o", dest="outfile", help="outfile", default="output")
	(options, args) = parser.parse_args()

	if not options.binfile:
		parser.print_help()
		sys.exit()
		
	try:
		FILE = open(options.binfile)
	except:
		print "unable to open binfile",options.binfile
		sys.exit()

	try:
		OUTFILE = open(options.outfile, 'w')
	except:
		print "unable to open outfile"
		sys.exit()

	for line in FILE.readlines():
		line = string.rstrip(line)	

		cols = line.split()
		seq  = cols[0]
		dist = float(cols[3])
		ene  = cols[4]
		seqi = seq[0:1]
		seqj = seq[1:2]
		
		if seqj < seqi:
			seq = seqj + seqi

		bindist = int((dist/float(options.bin)) + 0.5) * 0.5
		OUTFILE.write(seq + " " + str(bindist) + " " + ene + "\n")

	OUTFILE.close()

		

if __name__ == "__main__":
	main()
