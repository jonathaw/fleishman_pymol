#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import sys, os, string
from optparse import OptionParser
from file_routines import *


def main():

	"""
Renumbers ligand atoms starting at 9000
Useful when trying to select ligand atoms by their atom id
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
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

	het = re.compile("HETATM")

	for i in range(len(pdbfiles)):
		try:
			PDBFILE = open(pdbfiles[i])
		except:
			print "can't open pdbfile"
			sys.exit()

		mylines = PDBFILE.readlines()
		PDBFILE.close()

		try:
			OUTFILE = open(outfiles[i],'w')
		except:
			print "can't write to outfile"
			sys.exit()

		nat = 9000
		for line in mylines:
			newline = line
			if het.match(line):
				nat += 1
				nat = min(nat,9999)
				newline = "HETATM %4s%s"%(str(nat),line[11:])

			OUTFILE.write(newline)

		OUTFILE.close()


				






if __name__ == "__main__":
	main()
