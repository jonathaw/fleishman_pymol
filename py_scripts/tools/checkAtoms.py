#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from Molecule import *
from ProteinLibrary import *
from optparse import OptionParser
import os, sys, string



def main():

	"""
checks a pdbfile to see if all atoms of a given selection are present
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile",   help="pdbfile")
	parser.add_option("-P", dest="pdblist",   help="pdblist")
	parser.add_option("-b", dest="backbone",  help="backbone",  action="store_true")
	parser.add_option("-c", dest="centroid",  help="centroid",  action="store_true")
	parser.add_option("-f", dest="fullatom",  help="full-atom", action="store_true")
	parser.add_option("-s", dest="sidechain", help="sidechain", action="store_true")
	parser.add_option("-n", dest="number",    help="number only", action="store_true")
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

	home = os.environ['HOME']
	if options.centroid:
		libfile = home + "/py_scripts/data/centroids.lib"
	elif options.backbone:
		libfile = home + "/py_scripts/data/backbone.lib"
	elif options.sidechain:
		libfile = home + "/py_scripts/data/sidechains.lib"
	elif options.fullatom:
		libfile = home + "/py_scripts/data/all_atom.lib"
	else:
		libfile = home + "/py_scripts/data/centroids.lib"
		
		
	lib = ProteinLibrary()
	lib.readLibrary(libfile)

	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		nmissing = 0
		nres = 0
		for chain in protein.chain:
			for residue in chain.residue:
				resn = residue.name	
				nres += 1

				try:
					lib.residue[resn]
				except:
					#print "cannot find residue:",resn
					continue

				for atm in lib.residue[resn]:
					atom = residue.getAtom(atm)
					if not atom:
						if options.number:
							nmissing += 1
							break
						else:	
							print resn + residue.file_id + " -> |" + atm + "|"
		
		protein.clear()
		if options.number:
			print pdbfile,": ", nmissing,"missing out of",nres
					

		



if __name__ == "__main__":
	main()
