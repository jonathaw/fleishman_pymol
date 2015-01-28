#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import sys, os, string
from optparse import OptionParser
from Molecule import *
from file_routines import *


def main():

	"""
reads in and writes a pdbfile while renumbering the atoms and residues
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("--no_atom_renumber", dest="no_atrenum", help="don't renumber atoms", action="store_true")
	parser.add_option("--no_res_renumber", dest="no_resrenum", help="don't renumber residues", action="store_true")
	parser.add_option("--start_residue", dest="start_res", help="starting residue")
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

	start_res = 0
	bAtRenum = True
	bResRenum = True
	if options.no_atrenum:
		bAtRenum = False
	if options.no_resrenum:
		bResRenum = False
	if options.start_residue:
		start_res = int(options.start_residue)

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


	npdb = len(pdbfiles)
	nout = len(outfiles)

	if npdb != nout:
		print "number of pdbfiles and output files differ"
		sys.exit()

	protein = Molecule()	
	for i in range(len(pdbfiles)):
		protein.readPDB(pdbfiles[i])
		protein.writePDB(outfiles[i], resRenumber=bResRenum, atomRenumber=bAtRenum, start_res=start_res)
		protein.clear()




if __name__ == "__main__":
	main()
