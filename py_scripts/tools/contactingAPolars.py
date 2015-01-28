#!/usr/bin/python

from optparse import OptionParser
import os, sys, string, re, commands
from Enzyme import *
from Selection import *
from file_routines import *
from mol_routines import *

def main():

	"""
reports the residues with polar sidechain atoms contacting a given selection
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="selection",help="selection")
	parser.add_option("-c", dest="catalytic", help="catalytic")
	parser.add_option("-x", dest="cutoff", help="cutoff (default 3.5)", default=3.5)
	parser.add_option("-n", dest="number", help="number only", action="store_true")
	parser.add_option("--charged_only", dest="charged", help="charged residues only", action="store_true")
	parser.add_option("--ignore_catalytic", dest="no_cat", help="ignore catalytic residues", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	cutoff = float(options.cutoff)
	if not options.selection and not options.catalytic:
		parser.print_help()
		sys.exit()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	
	sele = Selection()
	if options.selection:
		sele.makeSelection(options.selection)

	protein = Enzyme()
	protSel = Selection()
	protSel.makeSelection("SC;type=ATOM  ")
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		if options.catalytic:
			icat = int(options.catalytic)
			if icat == 0 or icat > len(protein.catalytic):
				print "accessing catalytic out of bounds"
				sys.exit()
			mysel = protein.catalytic[icat-1].atomList()
		else:
			mysel = sele.apply_selection(protein).atomList()

		protAtoms = protSel.apply_selection(protein)
		nearby_atoms = atomsAroundAtoms(mysel, protAtoms, cutoff=cutoff)

		reslist = []
		for atm in nearby_atoms:
			if options.no_cat:
				catFound = False
				for cat in protein.catalytic:
					if int(atm.resi) == int(cat.file_id):
						catFound = True
						break
				if catFound:
					continue

			if not atm.parentResidue in reslist:
				reslist.append(atm.parentResidue)

		if options.number:
			print pdbfile,len(reslist)
		else:
			for res in reslist:
				#if options.charged:
				#	if res.name != "ARG" and res.name != "LYS" and res.name != "GLU" and res.name != "ASP":
				#		continue
				if res.name == "PHE" or res.name == "TRP" or res.name == "TYR" or res.name == "MET":
					print res.file_id,res.name
		

		protein.clear()
		


if __name__ == "__main__":
	main()
