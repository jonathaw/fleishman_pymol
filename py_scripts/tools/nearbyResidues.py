#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Molecule import *
from Selection import *

def main():

	"""
	prints a list of residues that are near to a selection
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-c", dest="cutoff", help="cutoff",default="5.0")
	parser.add_option("-r", dest="residue", help="residue")
	parser.add_option("-d", dest="delimited", help="comma delimited", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	if not options.selection:
		parser.print_help()
		sys.exit()
	

	sele = Selection()
	sele.makeSelection(options.selection)
	protein = Molecule()
	cut = float(options.cutoff)
	for pdbfile in pdbfiles:
		if not options.delimited:
			print pdbfile
		protein.readPDB(pdbfile)
		newmol = sele.apply_selection(protein)
		atmlist = newmol.atomList()

		nearby = []
		for atm in atmlist:
			results = residuesAroundAtom(atm, protein, cut)
			for a in results:
				if options.residue:
					if a.name == options.residue:
						if not (a in nearby):
							nearby.append(a)
				else:
					if not (a in nearby):
						nearby.append(a)

		if options.delimited:
			pp = ""
			ln = len(nearby)
			cn = 0
			for res in nearby:
				cn += 1
				pp += str(int(res.file_id))
				if cn < ln:
					pp += ","
			print pdbfile,pp
		else:
			for res in nearby:
				print res.name,res.file_id

		protein.clear()
		



if __name__ == "__main__":
	main()
