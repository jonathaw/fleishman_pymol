#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from surface_routines import *
from Enzyme import *
from Selection import *
from Hbond import *

def main():

	"""
reports the buried unsatisfied hydrogen bonds in a pdbfile.
REQUIRES NACCESS
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-c", dest="catalytic", help="catalytic")
	parser.add_option("-x", dest="cutoff", help="surface area cutoff", default=5.0)
	parser.add_option("-X", dest="hcutoff", help="hbond energy ctuoff", default=-0.1)
	parser.add_option("-r", dest="report", help="report number only", action="store_true")
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
	surfout = Molecule()
	sele = Selection()
	sele_string = ""
	if options.selection:
		sele.makeSelection(options.selection)
		sele_string += options.selection
	for pdbfile in pdbfiles:
		outlist = []
		protein.readPDB(pdbfile)
		catid = -1
		if options.catalytic:
			icat = int(options.catalytic) - 1
			if icat >= len(protein.catalytic):
				print "accessing catalytic out of bounds"
				continue
			catres = protein.catalytic[icat]
			catid = int(catres.file_id)

		HBN.createNetwork(protein)
		HE = float(options.hcutoff)
		HBN.findHbonds(cutoff=HE)
		unsat = HBN.unsatisfiedHbonds()

		get_surface_area(pdbfile, "surf")
		surfout.readPDB("surf.asa")

		if surfout.numResidues == 0:
			print "surf.asa not found"
			sys.exit()

		if options.selection:
			newMol = sele.apply_selection(mol=surfout)
			surfout.clear()
			newMol.clone(surfout)

		for atm in unsat:
			myres = surfout.getResidue(int(atm.resi))
			if myres == None:
				continue

			myatm = myres.getAtom(atm.name)
			if myatm == None:
				continue

			if catid != -1:
				if int(myres.file_id) != catid:
					continue

			if myatm.occupancy <= float(options.cutoff):
				outlist.append(myatm)

		if options.report:
			print pdbfile,len(outlist)
		else:
			for atm in outlist:
				print atm

		protein.clear()
		HBN.clear()
		surfout.clear()


	# clear out intermediate files
	os.system("rm -f surf.log")
	os.system("rm -f surf.pdb")
	os.system("rm -f surf.rsa")
	os.system("rm -f surf.asa")


if __name__ == "__main__":
	main()
