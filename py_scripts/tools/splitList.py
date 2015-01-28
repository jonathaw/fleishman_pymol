#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string, sys, os
from optparse import OptionParser


def main():

	"""
	splits a list for faster condor_submission
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="list", help="list of files")
	parser.add_option("-b", dest="nper", help="number per bin")
	parser.add_option("-n", dest="name", help="list name")
	parser.set_description(main.__doc__)


	(options, args) = parser.parse_args()

	if not options.list or not options.nper:
		parser.print_help()
		sys.exit()

	
	name = "list"
	if options.name != None:
		name = options.name

	try:
		PDBLIST = open(options.list)
	except:
		print "unable to open list"
		sys.exit()

	curr_num = 0
	ifile = 0
	nper = int(options.nper)
	for file in PDBLIST.readlines():
		file = string.strip(file)
		if ifile >= nper or ifile == 0:
			if ifile > 0:
				OUTPUT.close()

			try:
				newfile = name + "." + str(curr_num)
				OUTPUT = open(newfile, 'w')
			except:
				print "unable to open newfile"
				sys.exit()
			ifile = 0
			curr_num += 1

		OUTPUT.write(file + "\n")
		ifile += 1

	print curr_num 



if __name__ == "__main__":
	main()
