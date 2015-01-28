#!/usr/bin/python


from Molecule import *
from ProteinLibrary import *
from optparse import OptionParser
import os, sys, string, re
from mol_routines import *
from match_routines import *
from file_routines import *



def main():

	"""
	takes output from a -dump_ligand_only match file and puts the sidechain back into the scaffold
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="scaffold", help="scaffold")
	parser.add_option("-o", dest="outfile",  help="outfile")
	parser.add_option("-O", dest="outlist",  help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-i", dest="ignore", help="ignore catalytic residue (name)")
	parser.add_option("--check", dest="check", help="check for grafting", action="store_true")
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

	outfiles = []
	if options.outlist:
		outfiles = files_from_list(options.outlist)
	elif options.outfile:
		outfiles.append(options.outfile)
	elif options.replace:
		outfiles = pdbfiles
	else:
		parser.print_help()
		sys.exit()

	if not options.scaffold:
		parser.print_help()
		sys.exit()


	protein = Molecule()
	protein.readPDB(options.scaffold)
	scaffold = protein.chain[0]

	mol = Molecule()
	for i in range(len(pdbfiles)):
		print pdbfiles[i]
		chainA = scaffold.clone()
	
		mol.readPDB(pdbfiles[i])	
		chainB = mol.getChain("B")
		#chainB = mol.chain[0]
		cat = []
		cat = getCatalyticResidues(mol)
		if len(cat) == 0:
			sys.exit()

		if options.check:
			if mol.numResidues() > (len(cat) + 4):
				print pdbfiles[i],"already grafted"
				mol.clear()
				continue

		for res in cat:
			if options.ignore:
				if res.name == options.ignore:
					continue
			chainA.replaceResidue(res.file_id,res)

		chainA.renumber(resRenumber=False)

		mol.removeChain("B")
		mol.chain.insert(0,chainA)
		mol.writePDB(outfiles[i], resRenumber=False, atomRenumber=False)
		mol.clear()

		

if __name__ == "__main__":
	main()
