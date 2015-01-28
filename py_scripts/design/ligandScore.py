#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string, sys, os, commands
from optparse import OptionParser
from file_routines import *
from Enzyme import *


def main():

	"""
reports the ligand score (Eatr + Erep + EhbSC)
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
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
		
	protein = Enzyme()
	for file in pdbfiles:
		protein.readPDB(file)
		lig = protein.ligand
		if lig == None:
			print "no ligand found for file:",file
			sys.exit()

		tot = lig.Erep + lig.Eatr + lig.EhbSC
		print file,lig.Erep,lig.Eatr,lig.EhbSC,tot
		protein.clear()



if __name__ == "__main__":
	main()
