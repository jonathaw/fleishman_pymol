#!/usr/bin/python

import string, sys, re, os
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from surface_routines import *
from Enzyme import *
from Selection import *

def main():

	"""
returns the surface area of a protein (or selection).
REQUIRES EXTERNAL BINARY "NACCESS".
This looks for naccess in ~/code/naccess/nacess
or in /net/local/bin/naccess
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-c", dest="catalytic", help="catalytic")
	parser.add_option("-t", dest="total", help="report total surface area", action="store_true")
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

#	if not options.selection and not options.catalytic:
#		parser.print_help()
#		sys.exit()
	

	sasafile = Molecule()
	sele = Selection()
	if options.selection:
		sele.makeSelection(options.selection)

	enz = Enzyme()

	outbase = "clean"
	outpdb = outbase + ".asa"
	for pdbfile in pdbfiles:
	
		if options.catalytic:
			enz.readPDB(pdbfile)
			icat = int(options.catalytic) - 1
			cres = int(enz.catalytic[icat].file_id)
			newsele = "resi=" + str(cres)
			if options.selection:
				newsele += ";" + options.selection
			sele.clear()
			sele.makeSelection(newsele)
			enz.clear()
			
		get_surface_area(pdbfile, outbase)
		sasafile.readPDB(outpdb)
		if options.selection or options.catalytic:
			atmlist = sele.apply_selection(sasafile).atomList()
		else:
			atmlist = sasafile.atomList()

		if options.total:
			tot_sas = 0.0
			for atm in atmlist:
				tot_sas += atm.occupancy
			print pdbfile,":",tot_sas
		else:
			print pdbfile,":"
			for atm in atmlist:
				#print atm
				print atm.file_id,atm.name,atm.resn,atm.resi,atm.occupancy,atm.bfactor

		sasafile.clear()
		



if __name__ == "__main__":
	main()

