#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from Molecule import *
from ss_routines import *
from SecondaryStructure import *
from optparse import OptionParser
import sys, os, string



def main():

	"""
runs the dssp program to determine secondary structural content for a given protein
	"""
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-f", dest="format", help="format", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.pdbfile:
		parser.print_help()
		sys.exit()

	result = run_dssp(options.pdbfile)
	if result == -1:
		print "error running dssp"
		sys.exit()

	if options.format:
		ss = SecondaryStructure();
		ss.sequence = result
		ss.parse()
		ss.printSequence()
	else:
		print result



if __name__ == "__main__":
	main()
