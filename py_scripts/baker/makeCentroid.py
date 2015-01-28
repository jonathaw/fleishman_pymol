#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import os, string, sys, commands
from optparse import OptionParser

def main():

	"""
strips a pdbfile to its backbone and CB
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	exe  = "makeSelection.py" 
	sele = ' -s "CEN"'

	if options.pdbfile:
		exe += " -p " + options.pdbfile
	else:
		parser.print_help()
		sys.exit()

	if options.outfile:
		exe += " -o " + options.outfile
	elif options.replace:
		exe += " -r "
	else:
		parser.print_help()
		sys.exit()

	exe += sele

	os.system(exe)




if __name__ == '__main__':
	main()
