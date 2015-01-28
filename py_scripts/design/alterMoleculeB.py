#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import os, sys, string, commands
from optparse import OptionParser


def main():

	"""
changes the b-value of a pdbfile by setting the b-value to a fixed value
or incremementing the b-value or by sorting the pdbfile based on the b-value
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-s", dest="sort", help="sort", action="store_true")
	parser.add_option("-b", dest="bvalue", help="b value")
	parser.add_option("-i", dest="increment", help="increment", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		LIST = open(options.pdblist)
		for line in LIST.readlines():
			line = string.rstrip(line)
			pdbfiles.append(line)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()
	
	outfile = ""
	if options.outfile:
		if len(pdbfiles) > 1:
			print "can only use -P flag with -r"
			sys.exit()
		outfile = pdbfiles[0]
	elif options.replace:
		outfile = pdbfiles[0]
	else:
		parser.print_help()
		sys.exit()

	for pdbfile in pdbfiles:
		FILE = open(pdbfile)
		pdb = FILE.readlines()
		FILE.close()

		if options.replace:
			outfile = pdbfile

		pdb = filter(lambda x:x[0:6] in ("HETATM", "ATOM  "),pdb)	

		OUTPUT = open(outfile, 'w')
		if options.sort:
			pdb = map(lambda x:(float(x[60:66]),x),pdb)
			pdb.sort()
			pdb = map(lambda x:x[1], pdb)
			
			for line in pdb:
				OUTPUT.write(line)
		elif options.bvalue:
			for line in pdb:
				newline = line[0:60] + "%6.2f"%float(options.bvalue) + line[66:]
				OUTPUT.write(newline)
		elif options.increment:
			bvalue = 0.01
			for line in pdb:
				newline = line[0:60] + "%6.2f"%float(bvalue) + line[66:]
				OUTPUT.write(newline)
				bvalue += 0.01
		else:
			parser.print_help()
			sys.exit()

		OUTPUT.close()

			


if __name__ == "__main__":
	main()
