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
	parser.add_option("-a", dest="atoms", help="ligand atom ids's (comma separated)")
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

	if not options.atoms:
		parser.print_help()
		sys.exit()

	tmps = options.atoms.split(",")
	atms = []
	for i in tmps:
		atms.append(int(i))
		
	re_atm = re.compile("atm_id")
	for file in pdbfiles:
		try:
			PDB = open(file)
		except:
			print "unable to open pdbfile"
			sys.exit()

		bRead = False

		tot_atr = 0.0
		tot_rep = 0.0
		tot_hbd = 0.0
		tot_sas = 0.0
		tot_pak = 0.0
		for line in PDB.readlines():
			if re_atm.search(line):
				bRead = True
				continue

			if bRead:
				cols = line.split()
				if len(cols) == 0:
					bRead = False
					break

				if int(cols[0]) in atms:
					tot_atr += float(cols[3])
					tot_rep += float(cols[4])
					tot_hbd += float(cols[6])
					tot_sas += float(cols[7])
					tot_pak += float(cols[8])

		print file,tot_atr,tot_rep,tot_hbd,tot_sas,tot_pak
				
			



if __name__ == "__main__":
	main()
