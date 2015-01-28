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
reads a rosetta output pdbfile and reports residues that have a lig_dun > cutoff
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-x", dest="cutoff",  help="cutoff", default=3.0)
	parser.add_option("-s", dest="summary", help="summary", action="store_true")
	parser.add_option("-c", dest="catalytic", help="catalytic residues")
	parser.add_option("-l", dest="ligand", help="only ligand", action="store_true")
	parser.add_option("-n", dest="name", help="residue name (unique)")
	parser.add_option("-C", dest="catall", help="catalytic and ligand", action="store_true")
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
		tot_atr = 0
		max_val = -1

		catres = []
		if options.catall:
			for cat in protein.catalytic:
				catres.append(cat)

		if options.catalytic:
			icat = int(options.catalytic) - 1
			if icat >= len(protein.catalytic):
				print pdbfile, "catalytic out of bounds"
				sys.exit()
			catres.append(protein.catalytic[icat])


		if options.ligand or options.catall:
				catres.append(protein.ligand)

		if options.name:
			bCat = True
			catres = protein.getResiduesByName(options.name)
			if len(catres) != 1:
				print "too many catalytic residues"
				sys.exit()


		for chn in protein.chain:
			for res in chn.residue:
				if bCat:
					if not res in catres:
						continue

				edun = res.Edun
				if edun > cutoff:
					tot_value += edun
					max_val = max(max_val,edun)

					if options.summary:
						print pdbfile
						break
					else:
						print pdbfile,res.file_id,res.name,edun

		#print pdbfile,tot_value,max_val
			
		protein.clear()




if __name__ == "__main__":
	main()
