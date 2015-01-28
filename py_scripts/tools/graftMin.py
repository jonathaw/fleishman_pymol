#!/usr/bin/python


from Molecule import *
from ProteinLibrary import *
from optparse import OptionParser
import os, sys, string, re
from mol_routines import *
from file_routines import *
from match_routines import *



def main():

	"""
program that will graft old backed-up residues from matches into the corresponding
minimized pdbfile
	"""
	
	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-B", dest="backlist", help="backlist")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()


	if not options.pdblist or not options.backlist:
		parser.print_help()
		sys.exit()

	pdbfiles = files_from_list(options.pdblist)
	backfiles = files_from_list(options.backlist)
		
	protein = Molecule()
	backup = Molecule()
	for i in range(len(pdbfiles)):
		protein.readPDB(pdbfiles[i])
		backup.readPDB(backfiles[i])

		cat = getCatalyticResidues(protein)
		resi = 0
		for c in cat:
			if c.name == "GLU" or c.name == "ASP":
				resi = int(c.file_id)

		if resi == 0:
			print "cannot find glu or asp"
			sys.exit()

		probe = backup.getResidue(resi)	
		chainA = protein.getChain("A")	
		chainA.replaceResidue(resi, probe)
		protein.writePDB(pdbfiles[i], resRenumber=False, atomRenumber=False)

		protein.clear()
		backup.clear()
		
	
		


if __name__ == "__main__":
	main()
