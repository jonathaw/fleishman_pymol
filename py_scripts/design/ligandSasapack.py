#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string, sys, os, commands,re
from optparse import OptionParser
from file_routines import *


def main():

	"""
reports the ligand score (Eatr + Erep)
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
		
	re_sasa = re.compile("SASApack")
	for file in pdbfiles:
		try:
			PDB = open(file)
		except:
			print "unable to open pdbfile"
			sys.exit()

		bRead = False
		max_pack = 0.0
		tot_pack = 0.0
		tot_sasa = 0.0
		tot_sasa5 = 0.0
		for line in PDB.readlines():
			if re_sasa.search(line):
				bRead = True
				continue

			if bRead:
				cols = line.split()
				if len(cols) == 0:
					bRead = False
					break

				if cols[1] != "LG1":
					continue

				max_pack = max(max_pack,float(cols[9]))
				tot_pack += float(cols[9])
				tot_sasa += float(cols[8])
				tot_sasa5+= float(cols[7])

		print file,tot_pack,max_pack,tot_sasa,tot_sasa5
				
			



if __name__ == "__main__":
	main()
