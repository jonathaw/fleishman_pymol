#!/usr/bin/python


import os, sys, string, commands, re
from optparse import OptionParser
from Molecule import *

def main():
	parser = OptionParser()
	parser.add_option("-f", dest="binfile", help="binfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	(options, args) = parser.parse_args()

	if not options.binfile or not options.outfile:
		parser.print_help()
		sys.exit()

	try:
		FILE = open(options.binfile)
	except:
		print "unable to open binfile"
		sys.exit()

	results = {}
	for line in FILE.readlines():
		line = string.rstrip(line)	
		cols = line.split()

		seq  = cols[0]
		dist = cols[1]
		eab  = float(cols[2])

		if not seq in results.keys():
			results[seq] = {}

		if not dist in results[seq].keys():
			results[seq][dist] = []

		results[seq][dist].append(eab)

	try:
		OUTFILE = open(options.outfile, 'w')
	except:
		print "unable to open outfile"
		sys.exit()

	for seq in results.keys():
		for dist in results[seq].keys():
			n = len(results[seq][dist])
			avrg = 0.0
			for eab in results[seq][dist]:
				avrg += eab

			avrg/=float(n)

			rmsd = 0.0
			for eab in results[seq][dist]:
				rmsd += (eab - avrg)*(eab - avrg)
			rmsd /= float(n)
			rmsd = math.sqrt(rmsd)
				

			OUTFILE.write(seq + " " + dist + " " + str(n) + " " + str(avrg) + " " + str(rmsd) + "\n")

	OUTFILE.close()
				
	


if __name__ == "__main__":
	main()
