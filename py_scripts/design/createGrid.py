#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import os, sys, string, commands
from optparse import OptionParser
from mol_routines import *
from grid_functions import *
from Molecule import *
from Selection import *



def main():

	"""
creates a grid given a template of a previous grid
This creates a gridlig and a gridbb
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-s", dest="statefile", help="statefile")
	parser.add_option("-o", dest="outname", help="outname")
	parser.add_option("-l", dest="ligcutoff", help="gridlig cutoff", default=2.5)
	parser.add_option("-b", dest="bbcutoff", help="gridbb cutoff", default=2.0)
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.pdbfile or not options.statefile or not options.outname:
		parser.print_help()
		sys.exit()

	# get output filename
	cols = options.outname.split(".")
	outgridlig = cols[0] + ".gridlig"
	outgridbb = cols[0] + ".gridbb"

	# get backbone from protein
	protein = Molecule()
	protein.readPDB(options.pdbfile)
	
	sele = Selection()
	sele.makeSelection("BB")
	bb = sele.apply_selection(protein).atomList()

	# read in previous statefile information
	try:
		STATEFILE = open(options.statefile)
	except:
		print "unable to open statefile"
		sys.exit()

	gridlig_file = ""
	gridbb_file  = ""
	for line in STATEFILE.readlines():
		cols = line.split()
		if cols[0] == "gridlig:":
			gridlig_file = cols[1]
		if cols[0] == "gridbb:":
			gridbb_file = cols[1]

	gridlig = grid()
	gridbb  = grid()

	gridlig.read(gridlig_file)
	gridbb.read(gridbb_file)

	gridlig.setFullOccupied()
	gridbb.setFullOccupied()

	ligcutoff = float(options.ligcutoff)
	bbcutoff = float(options.bbcutoff)
	gridTrimInclude(gridbb, bb, bbcutoff)
	gridTrimExclude(gridlig, bb, ligcutoff)

	gridlig.write(outgridlig)
	gridbb.write(outgridbb)



if __name__ == "__main__":
	main()
