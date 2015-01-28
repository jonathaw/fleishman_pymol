#!/usr/bin/python

from Enzyme import *
from Selection import *
from optparse import OptionParser
import sys, string
from file_routines import *
from mol_routines import *


def main():

	"""
checks for clashes of atoms in catalytic residues to CB's of the protein
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("--total_cutoff", dest="total_cutoff", help="total clash cutoff (2)", default="2")
	parser.add_option("--indi_cutoff", dest="indi_cutoff", help="indi clash cutoff (1)", default="1")
	parser.add_option("-s", dest="scaffold", help="scaffold")
	parser.add_option("-E", dest="ss_file", help="secondary structure file")
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

	ss = ""
	if options.ss_file:
		try:
			SSFILE = open(options.ss_file)
		except:
			print "unable to open secondary structure file"
			sys.exit()

		for line in SSFILE:
			line = string.rstrip(line)
			ss = line

	sele = Selection()
	sele.makeSelection("name= CB ")

	scaff = Molecule()
	scaffold = None
	if options.scaffold:
		scaff.readPDB(options.scaffold)
		scaffold = sele.apply_selection(scaff)

		
	protein = Enzyme()
	for file in pdbfiles:
		protein.readPDB(file)

		centroid = None
		if options.scaffold:
			centroid = scaffold
		else:
			centroid = sele.apply_selection(protein)

		nres = centroid.numResidues()

		if options.ss_file:
			if len(ss) != nres:
				print "length of ss and pdbfile differ!",len(ss),nres
				sys.exit()
		else:
			ss = "E"*nres



		catlist = []
		for cat in protein.catalytic:
			myres = Residue()
			myres.name = cat.name
			myres.file_id = cat.file_id
			for atm in cat.atom:
				if atm.name != " N  " and atm.name != " CA " and atm.name != " C  " and atm.name != " O  ":
					myres.addAtom(atm)
			catlist.append(myres)


			
		max_indi_clash = 0
		nclash = 0
		outline = file
		for catres in catlist:
			n_indi_clash = 0
			nres = 0
			for res in centroid.chain[0].residue:
				if res.file_id == catres.file_id:
					continue

				if ss[nres] == "L":
					nres += 1
					continue

				nres += 1

				if bResidue_Residue_clash_check(catres, res,0.75):
					n_indi_clash += 1
					nclash += 1

			max_indi_clash = max(max_indi_clash,n_indi_clash)

			outline += " " + str(n_indi_clash)

		outline += " " + str(nclash)

		if nclash > int(options.total_cutoff):
			print outline
		elif max_indi_clash > int(options.indi_cutoff):
			print outline

		protein.clear()




if __name__ == "__main__":
	main()

