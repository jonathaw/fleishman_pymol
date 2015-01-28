#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from TIM import *
from Enzyme import *

def main():

	"""
	prints a list of positions of catalytic residues in TIM structures
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-U", dest="unique_id", help="unique id")
	parser.add_option("-t", dest="TIM", help="TIM file")
	parser.add_option("-c", dest="catres", help="catres")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	pdbfiles = []
	ids      = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	elif options.unique_id:
		try:
			unique = open(options.unique_id)
		except:
			print "unable to open list of unique ids"
			sys.exit()

		for line in unique.readlines():
			cols = line.split()
			ids.append(cols[1])
	else:
		parser.print_help()
		sys.exit()

	if not options.TIM or not options.catres:
		parser.print_help()
		sys.exit()

	cresi = int(options.catres) - 1

	timmeh = TIM()
	timmeh.readTIM(options.TIM)

	protein = Enzyme()
	taken = {}

	if len(pdbfiles) > 0:
		for pdbfile in pdbfiles:
			protein.readPDB(pdbfile)
			
			if cresi >= len(protein.catalytic):
				print "accessing catalytic residue out of bounds"
				sys.exit()

			resi = int(protein.catalytic[cresi].file_id)
			myseg = timmeh.correspondingSegment(resi)

			if not myseg in taken.keys():
				taken[myseg] = 1
			else:
				taken[myseg] += 1

			protein.clear()

	if len(ids) > 0:
		for id in ids:
			wrd = id.split("_")

			if cresi >= len(wrd):
				print "accessing catalytic residue out of bounds"
				sys.exit()

			resi = int(wrd[cresi][1:])
			myseg = timmeh.correspondingSegment(resi)

			if not myseg in taken.keys():
				taken[myseg] = 1
			else:
				taken[myseg] += 1


	for key in taken.keys():
		print key,"-",taken[key]
		


if __name__ == "__main__":
	main()
