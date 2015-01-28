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
runs the stride program on a pdbfile to determine its secondary structure
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-f", dest="format", help="format", action="store_true")
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		try:
			LIST = open(options.pdblist, 'r')
		except:
			print "unable to open pdblist"
			sys.exit()

		for line in LIST.readlines():
			line = string.strip(line)
			pdbfiles.append(line)

		LIST.close()
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()


	outfiles = []
	if options.outlist:
		try:
			OUT = open(options.outlist, 'r')
		except:
			print "unable to open outlist"
			sys.exit()

		for line in OUT.readlines():
			line = string.strip(line)
			outfiles.append(line)

		OUT.close()
		if len(outfiles) != len(pdbfiles):
			print "number of pdbfiles and outfiles differ"
			sys.exit()

	elif options.outfile:
		outfiles.append(options.outfile)
		if len(outfiles) != len(pdbfiles):
			print "number of pdbfiles and outfiles differ"
			sys.exit()


	for i in range(len(pdbfiles)):
		result = run_stride(pdbfiles[i])
		if result == -1:
			print "error running stride"
			sys.exit()

		outline = result
		if options.format:
			ss = SecondaryStructure();
			ss.sequence = result
			ss.parse()
			outline = ss.formatSequence()

		if len(outfiles) > 0:
			try:
				OUTFILE = open(outfiles[i], 'w')
			except:
				print "unable to open outfile:",outfiles[i]

			OUTFILE.write(outline + "\n")
			OUTFILE.close()
		else:
			print outline




if __name__ == "__main__":
	main()
