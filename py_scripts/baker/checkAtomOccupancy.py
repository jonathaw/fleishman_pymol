#!/usr/bin/python


__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


from Molecule import *
from optparse import OptionParser
import sys, os, string



def main():

	"""
checkAtomOccupancy: checks for and reports atoms that have missing occupancy
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()


	pdbfiles = []
	if options.pdblist:
		try:
			PDBLIST = open(options.pdblist)
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

		found = False
		for chain in protein.chain:
			for residue in chain.residue:
				for atom in residue.atom:
					if atom.occupancy <= 0.0:
						found = True
						print pdbfile + ":" + residue.name + residue.file_id + "  " + atom.name + "  " + str(atom.occupancy)

		if found:
			print ""


		protein.clear()



if __name__ == "__main__":
	main()
