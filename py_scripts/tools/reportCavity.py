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
reports cavities around selections
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-x", dest="cutoff",  help="cutoff", default=3.0)
	parser.add_option("-c", dest="catalytic", help="only catalytic residues")
	parser.add_option("-l", dest="ligand", help="only ligand", action="store_true")
	parser.add_option("-C", dest="catall", help="all catalytic residues", action="store_true")
	parser.add_option("-r", dest="radius", help="hole radius", default=1.4)
	parser.add_option("-s", dest="selection", help="selection")
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

	re_cluster = re.compile("COMMENT CavClust")

	sele = Selection()
	if options.selection:
		sele.makeSelection(options.selection)

	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)

		cat_id = []
		mysel = []
		if options.catalytic:
			icat = int(options.catalytic) -1
			if icat < 0 or icat >= len(protein.catalytic):
				print "accessing catalytic out of bounds"
				sys.exit()
			mysel.append(protein.catalytic[icat])
		elif options.catall:
			for cat in protein.catalytic:
				mysel.append(cat)

		if options.ligand:
			for res in protein.chain[0].residue:
				if res.name == "LG1":
					mysel.append(res)

		if options.selection:
			tmp = sele.apply_selection(protein)
			for chn in tmp.chain:
				for res in chn.residue:
					mysel.append(res)
				

		# get cavities
		cavities = []
		for chn in protein.chain:
			for res in chn.residue:
				if res.name == "WSS":
					cavities.append(res)

		cav_atom_list = []
		for res in cavities:
			for atm in res.atom:
				cav_atom_list.append(atm)

		sel_atom_list = []
		for res in mysel:
			for atm in res.atom:
				sel_atom_list.append(atm)

		nearby_cav_atoms = atomsAroundAtoms(sel_atom_list, atomList=cav_atom_list, cutoff=cutoff)
		cav_res = []
		for atm in nearby_cav_atoms:
			if not atm.parentResidue in cav_res:
				cav_res.append(atm.parentResidue)

		# get cavities
		chainZ = protein.getChain("Z")
		if chainZ == None:
			print "cant' find chain Z"
			sys.exit()

		pdb_cav_list = []
		icav = 1
		for res in chainZ.residue:
			if res in cav_res:
				pdb_cav_list.append(icav)
			icav += 1

		protein.clear()

		try:
			PDBFILE = open(pdbfile)
		except:
			print "can't open pdbfile"
			sys.exit()

		tot_vol = 0.0
		for line in PDBFILE.readlines():
			if re_cluster.match(line):
				cols = line.split()
				if int(cols[2]) in pdb_cav_list:
					tot_vol += float(cols[5])

		print pdbfile,len(cav_res),tot_vol

		PDBFILE.close()



if __name__ == "__main__":
	main()
