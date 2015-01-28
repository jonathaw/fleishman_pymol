#!/usr/bin/python

import string, sys, re, os, commands
from optparse import OptionParser
from file_routines import *

def main():

	"""
	makes sure that asp or glu have 2 hbonds
	"""

	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-x", dest="cutoff", help="cutoff", default=-0.3)
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.pdblist:
		parser.print_help()
		sys.exit()

	pdbfiles = []
	pdbfiles = files_from_list(options.pdblist)

	for file in pdbfiles:
		exe = "checkHbonds.py -p " + file + " -x " + str(options.cutoff)
		ans = commands.getoutput(exe)
		lines = ans.split("\n")

		OD1found = False
		OD2found = False
		OE1found = False
		OE2found = False
		for line in lines:
			cols = line.split()
			if len(cols) < 8:
				continue

			if cols[8] == "OD1":
				OD1found = True
			if cols[8] == "OD2":
				OD2found = True
			if cols[8] == "OE1":
				OE1found = True
			if cols[8] == "OE2":
				OE2found = True

		keep = False
		if OD1found and OD2found:
			keep = True
		if OE1found and OE2found:
			keep = True

		if not keep:
			if not options.inverse:
				print file

		if keep:
			if options.inverse:
				print file

		




if __name__ == "__main__":
	main()
