#!/usr/bin/python

import os, string, sys
from optparse import OptionParser
from Molecule import *
from pdb_routines import *
from file_routines import *

def main():
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-c", dest="chain",   help="chain")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	outfiles = []
	if options.outlist:
		try:
			OUTLIST = open(outlist, 'r')
		except:
			print "unable to open file: ",outlist
			sys.exit()

		for line in OUTLIST.readlines():
			line = string.strip(line)
			outfiles.append(line)
	elif options.outfile:
		outfiles.append(options.outfile)
	elif options.replace:
		for file in pdbfiles:
			outfiles.append(file)
	else:
		parser.print_help()
		sys.exit()

	if len(pdbfiles) != len(outfiles):
		print "number of pdbfiles and outfiles differ"
		sys.exit()

	if not options.chain:
		parser.print_help()
		sys.exit()

	protein = Molecule()
	for i in range(len(pdbfiles)):
		protein.readPDB(pdbfiles[i])
		for chain in protein.chain:
			chain.name = options.chain

		protein.writePDB(outfiles[i])
		protein.clear()
		


if __name__ == '__main__':
	main()
