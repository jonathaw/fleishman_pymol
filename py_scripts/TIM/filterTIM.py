#!/usr/bin/python


import os, sys, string, commands
from optparse import OptionParser
from mol_routines import *
from Molecule import *
from Selection import *


def main():
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-c", dest="cut", help="cut")
	parser.add_option("-s", dest="size", help="size")
	parser.add_option("-o", dest="out", help="outfile")
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		try:
			PDBLIST = open(options.pdblist, 'r')
		except:
			print "unable to open pdblist"
			sys.exit()

		for line in PDBLIST.readlines():
			line = string.rstrip(line)
			pdbfiles.append(line)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()


	if options.out:
		try:
			OUT = open(options.out, 'w')
		except:
			print "unable to create outfile"
			sys.exit()
	else:
		parser.print_help()
		sys.exit()

		

	cutoff = 6.0
	if options.cut:
		cutoff = float(options.cut)

	minSize = 0
	maxSize = 1000
	if options.size:
		[minSize, maxSize] = options.size.split("-")
		minSize = int(minSize)
		maxSize = int(maxSize)


	protein = Molecule()
	for pdbfile in pdbfiles:
		ans = commands.getoutput("grep INSERT " + pdbfile)	
		cols = ans.split()
		res0 = int(cols[3])
		res1 = int(cols[4])
		res2 = res1 + 1

		size = res1 - res0 + 1
		if size < minSize or size > maxSize:
			continue

		protein.readPDB(pdbfile)	

		atom1 = protein.chain[0].getResidue(res1).getAtom(" C  ")
		atom2 = protein.chain[0].getResidue(res2).getAtom(" N  ")

		dist = atom1.distance(atom2)
		if dist < cutoff:
			OUT.write(pdbfile + "\n")

		protein.clear()

	OUT.close()



if __name__ == "__main__":
	main()
