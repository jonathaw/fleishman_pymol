#!/usr/bin/python


from Molecule import *
from Selection import *
from optparse import OptionParser
import os, sys, string, re
from mol_routines import *
from file_routines import *



def main():

	"""
	takes a ligand and grafts it into another pdbfile after a superimposition
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-l", dest="ligand", help="ligand")
	parser.add_option("-s", dest="protein_selection", help="protein selection")
	parser.add_option("-t", dest="ligand_selection", help="ligand selection")
	parser.add_option("-o", dest="outfile",  help="outfile")
	parser.add_option("-O", dest="outlist",  help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	# setup files
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

	if not options.ligand:
		parser.print_help()
		sys.exit()

	if len(pdbfiles) != len(outfiles):
		print "number of files differ"
		sys.exit()


	# get selections
	if not options.protein_selection or not options.ligand_selection:
		parser.print_help()
		sys.exit()


	sele = Selection()
	ligselection = "HET;" + options.ligand_selection
	sele.makeSelection(ligselection)
	ligMol = Molecule()
	ligMol.readPDB(options.ligand)
	ligand = sele.apply_selection(ligMol)

	if ligand.numResidues() != 1:
		print "ligand does not contain 1 residue"
		print ligand.numResidues()
		sys.exit()


	target = Molecule()
	sele.clear()
	sele.makeSelection(options.protein_selection)
	for i in range(len(pdbfiles)):
		print pdbfiles[i]
		target.readPDB(pdbfiles[i])
		tar = sele.apply_selection(target)
		ligMol2 = ligMol.clone()
		superimpose_molecule(tar,ligand,ligMol2)

		# graft new ligand onto existing target
		ligRes   = ligMol2.chain[0].residue[0]
		ligChain = target.chain[1]
		ligChain.clear()
		ligChain.addResidue(ligRes)

		if target.numChains() > 2:
			for j in range(2,target.numChains()):
				target.chain[j].clear()

		target.writePDB(outfiles[i],resRenumber=False)
		target.clear()
		ligMol2.clear()


if __name__ == "__main__":
	main()
