#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Enzyme import *
from Selection import *
from Hbond import *

def main():

	"""
checks for hydrogen bonds to ligands.  Ligands differ because we don't know
the acceptor antecedants
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-a", dest="acceptors", help="ligand acceptors")
	parser.add_option("-d", dest="donors", help="ligand donors")
	parser.add_option("-c", dest="catalytic", help="catalytic")
	parser.add_option("-x", dest="cutoff", help="cutoff", default=-0.3)
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

	protein = Enzyme()
	HBN = HBnetwork()

	if options.donors:
		donor_sel = Selection()
		donor_sel.makeSelection(options.donors)

	if options.acceptors:
		acceptor_sel = Selection()
		acceptor_sel.makeSelection(options.acceptors)

	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)

		ligands = protein.getHeteroAtoms()
		lig = ligands[0]

		residues = []
		if options.catalytic:
			cres = protein.catalytic[int(options.catalytic)-1]
			#cres = getCatalyticResidue(protein,int(options.catalytic))
			if cres == None:
				print "unable to find catalytic residue!"
				sys.exit()
			residues.append(cres)
		else:
			residues = protein.residueList()

		HBN.createNetwork(reslist=residues)
		if options.donors:
			donors = donor_sel.apply_selection(protein).atomList()

		if options.acceptors:
			acceptors = acceptor_sel.apply_selection(protein).atomList()
			if len(acceptors) == 0:
				print "unable to find acceptors"
				sys.exit()
			for a in acceptors:
				HBN.newAcceptor(A=a, res=lig)

		HBN.findHbonds(cutoff=float(options.cutoff),function=1)

		hblist = HBN.getHbondsToResidue(lig)
		if len(hblist) > 0:
			for Hb in hblist:
				print pdbfile,Hb
		else:
			print pdbfile," none"

		HBN.clear()
		protein.clear()




if __name__ == "__main__":
	main()
