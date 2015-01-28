#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from InteractionGraph import *
from pdb_routines import *

def main():

	"""
	creates a rosetta res file from an IG
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file or not options.outfile or not options.pdbfile:
		parser.print_help()
		sys.exit()
	
	IG = InteractionGraph()
	IG.read(options.file)

	Protein = Molecule()
	Protein.readPDB(options.pdbfile)

	nres = Protein.numResidues()

	try:
		OUTPUT = open(options.outfile, 'w')
	except:
		print "unable to open outfile"
		sys.exit()

	OUTPUT.write("""This file specifies which residues will be varied

 Column   2:  Chain
 Column   4-7:  sequential residue number
 Column   9-12:  pdb residue number
 Column  14-18: id  (described below)
 Column  20-40: amino acids to be used

 NATAA  => use native amino acid
 ALLAA  => all amino acids
 NATRO  => native amino acid and rotamer
 PIKAA  => select inividual amino acids
 POLAR  => polar amino acids
 APOLA  => apolar amino acids

 The following demo lines are in the proper format

 A    1    3 NATAA
 A    2    4 ALLAA
 A    3    6 NATRO
 A    4    7 NATAA
 B    5    1 PIKAA  DFLM
 B    6    2 PIKAA  HIL
 B    7    3 POLAR""")
	OUTPUT.write("\n -------------------------------------------------\n")
	OUTPUT.write(" start\n")

	# --- check which residues are allowed at each position --- #
	residues = {}
	for rot in IG.rotamers:
		aatype = rot.aatype
		seqpos = rot.seqpos
		if not residues.has_key(seqpos):
			residues[seqpos] = {}

		if not residues[seqpos].has_key(aatype):
			residues[seqpos][aatype] = True

	for i in range(1,nres+1):
		if residues.has_key(i):
			OUTPUT.write(" A%5d%5d PIKAA  " % (i,i))
			for key in residues[i].keys():
				OUTPUT.write(aa1_from_num(key))	
			OUTPUT.write("\n")
		else:
			OUTPUT.write(" A%5d%5d NATRO\n" % (i,i))

	OUTPUT.close()

	

	
		


if __name__ == "__main__":
	main()
