#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import os, sys, string, commands
from optparse import OptionParser
from mol_routines import *
from Molecule import *
from Selection import *


def main():

	"""
aligns two molecules that have differing number of atoms using the mammoth routine
	"""

	parser = OptionParser()
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-p", dest="probe", help="probe")
	parser.add_option("-P", dest="probelist", help="probelist")
	parser.add_option("-R", dest="rvalue", help="rvalue")
	parser.add_option("-o", dest="output", help="output")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.target or not options.output:
		parser.print_help()
		sys.exit()


	pdbfiles = []
	if options.probelist:
		try:
			LIST = open(options.probelist, 'r')
		except:
			print "unable to open list"
			sys.exit()
		
		for line in LIST.readlines():
			line = string.rstrip(line)
			pdbfiles.append(line)
	elif options.probe:
		pdbfiles.append(options.probe)
	else:
		parser.print_help()
		sys.exit()

	try:
		OUT = open(options.output, 'w')
	except:
		print "unable to create output"
		sys.exit()

	psi = 0
	for pdbfile in pdbfiles:
		print pdbfile
		if options.rvalue:
			outmol, psi, rms = mammoth(options.target, pdbfile, options.rvalue)
		else:
			outmol, psi, rms = mammoth(options.target, pdbfile)

		[base, suffix] = pdbfile.split(".",1)		
		newfile = base + "_align.pdb"
		outmol.writePDB(newfile)
		OUT.write(pdbfile + ": " + psi + "%; " + rms + "\n")



if __name__ == "__main__":
	main()
