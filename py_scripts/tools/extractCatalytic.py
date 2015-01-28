#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from Selection import *

def main():

	"""
given a match output file creates an output file of the catalytic site only
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.outfile or not options.pdbfile:
		parser.print_help()
		sys.exit()

	# read remark
	remark = re.compile("REMARK")
	try:
		pdb = open(options.pdbfile)
	except:
		print "unable to open pdbfile"
		sys.exit()


	resline = "resi="
	read = False
	for line in pdb.readlines():
		if remark.match(line):
			cols = line.split()
			resi = cols[5]
			if read:
				resline += ","
			resline += resi
			read = True

	pdb.close()

	selection = Selection()
	selection.makeSelection(resline)

	# ---   extract out the residue selections   --- #
	protein = Molecule()
	protein.readPDB(options.pdbfile)
	newmol = selection.apply_selection(protein)
	selection.clear()

	# ---   extract out the hetero atoms   --- #
	selection.makeSelection("type=HETATM")
	hetatm = selection.apply_selection(protein)
	reslist = hetatm.residueList()

	newchain = newmol.newChain()
	newchain.addResidueList(reslist)	
	
	newmol.writePDB("dumb.pdb")



if __name__ == "__main__":
	main()
