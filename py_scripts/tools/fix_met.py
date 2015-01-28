#!/usr/bin/python

import os, string, sys
from optparse import OptionParser
from Molecule import *
from pdb_routines import *
from file_routines import *

def main():

	"""
changes MSE residues to MET that are found in crystal structures
	"""
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
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
		outfiles = files_from_list(options.outlist)
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

	protein = Molecule()
	for i in range(len(pdbfiles)):
		protein.readPDB(pdbfiles[i])
		fixMet(protein)
		protein.writePDB(outfiles[i])
		protein.clear()
		


if __name__ == '__main__':
	main()
