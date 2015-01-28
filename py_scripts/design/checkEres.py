#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Enzyme import *
from Selection import *

def main():

	"""
reads a rosetta output pdbfile and reports residues that have a total Eres  > cutoff
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-x", dest="cutoff",  help="cutoff", default=3.0)
	parser.add_option("-s", dest="summary", help="summary", action="store_true")
	parser.add_option("-c", dest="catalytic", help="only catalytic residues", action="store_true")
	parser.add_option("-l", dest="ligand", help="only ligand", action="store_true")
	parser.add_option("-C", dest="catall", help="catalytic and ligand", action="store_true")
	parser.add_option("-t", dest="total", help="total", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	cutoff = float(options.cutoff)

	bCat = False
	if options.catalytic or options.ligand or options.catall:
		bCat = True

	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		tot_value = 0

		catres = []
		if options.catalytic or options.catall:
			for cat in protein.catalytic:
				catres.append(cat)

		if options.ligand or options.catall:
			catres.append(protein.ligand)

		for chn in protein.chain:
			for res in chn.residue:

				if bCat:
					if not res in catres:
						continue

				if res.Erep > cutoff:
					tot_value += res.Eres

					if options.summary:
						print pdbfile
						break

					if not options.total:
						print pdbfile,res.name,res.file_id,res.Eres
			
		if options.total:
			print pdbfile,tot_value

		protein.clear()




if __name__ == "__main__":
	main()
