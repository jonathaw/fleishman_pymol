#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from optparse import OptionParser
from Molecule import *
import os, sys, string


def main():

	"""
checks for and reports chain breaks.  Breaks are identified based on N-C distances
in the protein backbone
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		try:
			PDBLIST = open(options.pdblist, 'r')
		except:
			print "unable to open pdblist"
			sys.exit()

		for line in PDBLIST.readlines():
			line = string.strip(line)			
			pdbfiles.append(line)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	
	protein = Molecule()

	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)

		atomC = 0
		for chain in protein.chain:
			for res in chain.residue:
				prevC = atomC
				for atom in res.atom:
					
					if atom.name == " C  ":
						atomC = atom
					if atom.name == " N  ":
						atomN = atom

						if prevC != 0:
							dist = atomN.distance(atomC)

							if dist > 4.0:
								print pdbfile,"chain break on residue",res.file_id

		protein.clear()


if __name__ == "__main__":
	main()
