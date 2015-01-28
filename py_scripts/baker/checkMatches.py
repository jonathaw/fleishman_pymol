#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from Molecule import *
from optparse import OptionParser
import os, sys, string



def main():

	"""
checks enzyme design matches to see if the ligand is within the backbone grids
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="statefile", help="statefile")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		try:
			PDBLIST = open(options.pdblist)
		except:
			print "unable to open pdblist",options.pdblist
			sys.exit()

		for line in PDBLIST.readlines():
			line = string.strip(line)
			pdbfiles.append(line)	

	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	if not options.statefile:
		parser.print_help()


	gridlig = grid()
	gridbb  = grid()

	try:
		STATEFILE = open(options.statefile)
	except:
		print "unable to open statefile"
		sys.exit()

	for line in STATEFILE.readlines():
		line = string.strip(line)
		words = string.split(line)
		
		if "gridlig" in line:
			gridlig.read(words[1])

		if "gridbb" in line:
			gridbb.read(words[1])
			
		
	protein = Molecule()
	for pdbfile in pdbfiles:
		protein.clear()
		protein.readPDB(pdbfile)

		failed = False
		for chain in protein.chain:
			for residue in chain.residue:
				for atom in residue.atom:
					
					if atom.kind == "HETATM":
						if atom.name[0] == "V":
							continue

						x = atom.coord.x
						y = atom.coord.y
						z = atom.coord.z
						occ = atom.occupancy
		
						if occ > 0.0:
							if not gridlig.isInGrid(x, y, z):
								print pdbfile,atom.name,atom.file_id,"out of gridlig boundaries"
								failed = True
								continue

							zn = gridlig.getZone(x,y,z)	
							if not gridlig.zone[zn[0]][zn[1]][zn[2]]:
								print pdbfile,atom.name,atom.file_id,"not occupied in gridlig"
								failed = True
								continue

						if not gridbb.isInGrid(x,y,z):
							continue

						zn = gridbb.getZone(x,y,z)
						if gridbb.zone[zn[0]][zn[1]][zn[2]]:
							print pdbfile,atom.name,atom.file_id,"clashes with backbone"
							failed = True
							continue

		if not failed:
			print pdbfile,".... passes"



if __name__ == "__main__":
	main()
