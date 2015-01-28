#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from Molecule import *
from SecondaryStructure import *
from optparse import OptionParser
import sys, os, string


def main():

	"""
gets the secondary structural content of a protein read from a rosetta output file
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-s", dest="summary", help="summary", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	
	pdbfiles = []
	if options.pdblist:
		try:
			PDBLIST = open(options.pdblist, 'r')
		except:
			print "unable to open pdblist"
			sys.exit()

		for line in PDBLIST.readlines():
			line = string.strip(line)
			pdbfiles.append(line)	

	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()


	outfiles = []
	if options.outlist:
		try:
			OUTLIST = open(options.outlist, 'r')
		except:
			print "unable to open outlist"
			sys.exit()

		for line in OUTLIST.readlines():
			line = string.strip(line)
			outfiles.append(line)	

	elif options.outfile:
		outfiles.append(options.outfile)
	else:
		parser.print_help()
		sys.exit()

	if len(outfiles) != len(pdbfiles):
		print "number of input and output files differ"
		sys.exit()


	protein = Molecule()
	secstruct = SecondaryStructure()	
	for i in range(len(pdbfiles)):
		protein.readRosetta(pdbfiles[i])

		ss = ""	
		for chain in protein.chain:
			for residue in chain.residue:
				ss += residue.ss

		if options.summary:
			secstruct.sequence = ss
			myss = secstruct.formatSequence()

			try:
				OUT = open(outfiles[i], 'w')
			except:
				print "unable to open outfile"

			OUT.write(myss + "\n")
			OUT.close()

		protein.clear()


if __name__ == "__main__":
	main()
