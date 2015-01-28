#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string, sys, os, commands,re
from optparse import OptionParser
from file_routines import *


def main():

	"""
reports the ligand interface energies
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-x", dest="cutoff", help="cutoff (2.0)", default=2.0)
	parser.add_option("-s", dest="summary", help="summary", action="store_true")
	parser.add_option("-t", dest="total", help="total", action="store_true")
	parser.add_option("--ignore", dest="ignore", help="number of worst contacts to ignore")
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

	re_int = re.compile("interface")
	cutoff = float(options.cutoff)
	for file in pdbfiles:
		try:
			PDB = open(file)
		except:
			print "unable to open pdbfile"
			sys.exit()

		bRead = False

		Eatr = []
		Erep = []
		name = []
		nclash = 0
		for line in PDB.readlines():
			if re_int.search(line):
				bRead = True
				continue

			if bRead:
				cols = line.split()
				if cols[0] == "res1":
					continue

				if cols[0] == "SCORE":
					bRead = False
					break

				name.append(cols[2])
				Eatr.append(float(cols[5]))
				Erep.append(float(cols[6]))

		max_cutoff = 9999999
		if options.ignore:
			new_rep = []
			for e in Erep:
				new_rep.append(e)
			new_rep.sort()
			new_rep.reverse()
			ni = int(options.ignore)
			if ni >= len(Erep):
				ni = len(Erep)

			ni -= 1
			max_cutoff = new_rep[ni]

		tot_atr = 0.0
		tot_rep = 0.0
		for i in range(len(Erep)):
			if Erep[i] > cutoff and Erep[i] < max_cutoff:
				if options.summary:
					nclash += 1
				elif options.total:
					tot_atr += Eatr[i]
					tot_rep += Erep[i]
					nclash += 1
				else:
					print file,name[i],Eatr[i],Erep[i]
				
		if options.summary:
			print file,nclash
		elif options.total:
			print file,tot_atr,tot_rep,nclash

				
			



if __name__ == "__main__":
	main()
