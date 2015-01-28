#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string, sys, os
from optparse import OptionParser


def main():

	"""
creates sets of directories and fills them with files from a list
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="list", help="list of files")
	parser.add_option("-b", dest="nper", help="number per bin")
	parser.add_option("-n", dest="name", help="base name")
	parser.add_option("-p", dest="nbin", help="number of bins")
	parser.set_description(main.__doc__)


	(options, args) = parser.parse_args()

	if options.list == None:
		parser.print_help()

	
	name = "set"
	if options.name != None:
		name = options.name

	try:
		PDBLIST = open(options.list)
	except:
		print "unable to open list"
		sys.exit()

	files = []
	for file in PDBLIST.readlines():
		file = string.strip(file)
		files.append(file)

	if len(files) == 0:
		sys.exit()
	
	nper = 0
	if options.nper:
		nper = int(options.nper)
	elif options.nbin != None:
		nper = int(len(files)/int(options.nbin))+1
	else:
		parser.print_help()
		sys.exit()


	
	nsets = 0
	mydir = name + str(nsets)
	count = 0
	os.system("mkdir " + mydir)
	for file in files:
		if count == nper:
			nsets += 1
			mydir = name + str(nsets)
			os.system("mkdir " + mydir)
			count = 0

		move = "mv " + file + " " + mydir
		os.system(move)
		count += 1



if __name__ == "__main__":
	main()
