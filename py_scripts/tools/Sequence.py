#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from optparse import OptionParser
from Molecule import *
from Selection import *
from file_routines import *
import sys, os, string


def main():

	"""
reads in a pdbfile and writes out the protein sequence
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-t", dest="transpose", help="transpose", action="store_true")
	parser.add_option("-n", dest="number", help="number", action="store_true")
	parser.add_option("-r", dest="range", help="range")
	parser.add_option("-s", dest="selection", help="selection")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)	
	else:
		parser.print_help()
		sys.exit()

	
	if options.selection:
		sele = Selection()
		sele.makeSelection(options.selection)

	seq_min = 1
	seq_max = 1
	if options.range:
		(min,max) = string.split(arg, "-")
		seq_min = int(min)
		seq_max = int(max)

	protein = Molecule()
	Seq = ""
	for pdb in pdbfiles:
		protein.readPDB(pdb)
		if options.selection:
			newmol = sele.apply_selection(protein)
			Seq = newmol.sequence()
		else:
			Seq = protein.sequence()

		if options.range:
			Seq = Seq[seq_min:seq_max]

		if options.transpose:
			for i in range(len(Seq)):
				print Seq[i]
		else:
			print Seq

		protein.clear()

		


if __name__ == '__main__':
	main()
