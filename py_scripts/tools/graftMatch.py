#!/usr/bin/python


from Molecule import *
from ProteinLibrary import *
from optparse import OptionParser
import os, sys, string, re
from mol_routines import *



def main():

	"""
program to graft matching sidechains from a mabo-formatted pdbfile  back into the protein
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="output",  help="output")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()


	if not options.pdbfile or not options.output:
		parser.print_help()
		sys.exit()

	protein = Molecule()
	protein.readPDB(options.pdbfile)


	# --- check in the remarks section which sidechain to graft
	template = re.compile("TEMPLATE")

	# --- grab the catalytic site and hetero atoms
	cat_site = []
	for line in protein.remark:
		if template.search(line):
			cols = line.split()
			cat_site.append(cols[5])

	chainA = protein.chain[0]
	chainB = protein.getChain("B")
	if chainB.numResidues() != len(cat_site):
		print "ERROR: number of residues in chain B != cat_site"
		sys.exit()

	for i in range(chainB.numResidues()):
		chainA.replaceResidue(cat_site[i], chainB.residue[i])
		

	protein.writePDB(options.output)
	
		


if __name__ == "__main__":
	main()
