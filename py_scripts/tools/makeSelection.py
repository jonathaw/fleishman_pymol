#!/usr/bin/python

from Enzyme import *
from Selection import *
from optparse import OptionParser
import sys, string
from file_routines import *


def main():

	"""
creates a new pdbfile from a given selection (almost pymol-like selection format)
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true")
	parser.add_option("-n", dest="renumber", help="don't renumber residues", action="store_true")
	parser.add_option("-c", dest="count", help="report atom count only", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()


	pdbfiles = []
	outfiles = []
	if not options.selection:
		parser.print_help()
		sys.exit()

	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()


	bFileOutput = True
	if options.outlist:
		outfiles = files_from_list(options.outlist)
	elif options.outfile:
		outfiles.append(options.outfile)
	elif options.replace:
		for file in pdbfiles:
			outfiles.append(file)
	else:
		bFileOutput = False

	selection = Selection()	
	selection.makeSelection(options.selection)

	protein = Enzyme()

	resRenumber = True
	if options.renumber:
		resRenumber = False
	for i in range(len(pdbfiles)):
		protein.readPDB(pdbfiles[i])
		newmol  = selection.apply_selection(protein)
		if options.count:
			print newmol.numAtoms()
		elif bFileOutput:
			newmol.writePDB(outfiles[i],resRenumber)
		else:
			for atm in newmol.atomList():
				print atm

		protein.clear()
		newmol.clear()



if __name__ == "__main__":
	main()

