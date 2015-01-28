#!/usr/bin/python

from Molecule import *
from optparse import OptionParser
import os, string, sys


def main():

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	(options, args) = parser.parse_args()

	if not options.pdbfile:
		parser.print_help()
		sys.exit()

	mol = Molecule()
	mol.readPDB(options.pdbfile)

	for chain in mol.chain:
		for res in chain.residue:
			for atom in res.atom:
				print "|" + atom.name + "|" + atom.element


if __name__ == "__main__":
	main()
