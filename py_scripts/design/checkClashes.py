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
reads a rosetta output pdbfile and reports residues that have a lig_rep > cutoff
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-x", dest="cutoff",  help="cutoff", default=3.0)
	parser.add_option("-s", dest="summary", help="summary", action="store_true")
	parser.add_option("-c", dest="catalytic", help="catalytic residues", action="store_true")
	parser.add_option("-l", dest="ligand", help="only ligand", action="store_true")
	parser.add_option("-n", dest="name", help="residue name (unique)")
	parser.add_option("-C", dest="catall", help="catalytic and ligand", action="store_true")
	parser.add_option("-t", dest="total", help="total", action="store_true")
	parser.add_option("-r", dest="radius", help="include residues within radius")
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

	bRad = False
	if options.radius:
		bRad = True
		rad_cutoff = float(options.radius)

	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		tot_value = 0
		tot_atr = 0

		catres = []
		if options.catalytic or options.catall:
			for cat in protein.catalytic:
				catres.append(cat)

		if options.ligand or options.catall:
				catres.append(protein.ligand)

		if options.name:
			bCat = True
			catres = protein.getResiduesByName(options.name)
			if len(catres) != 1:
				print "too many catalytic residues"
				sys.exit()


		for chn in protein.chain:
			if bRad:
				ligAtms = protein.ligand.atom
				near_res = residuesAroundAtoms(ligAtms, protein, rad_cutoff)

			for res in chn.residue:

				if bCat and not bRad:
					if not res in catres:
						continue

				if bRad:
					if not res in catres:
						if not res in near_res:
							continue

				erep = res.Erep
				if erep > cutoff:
					tot_value += erep
					tot_atr += res.Eatr

					if options.summary:
						print pdbfile
						break

					if not options.total:
						myE = res.Erep + res.Eatr + res.EhbSC + res.Esol + res.Edun
						print pdbfile,res.name,res.file_id,res.Erep,res.Eatr,res.EhbSC,res.Esol,res.Edun,myE
			
		if options.total:
			print pdbfile,tot_value,tot_atr

		protein.clear()




if __name__ == "__main__":
	main()
