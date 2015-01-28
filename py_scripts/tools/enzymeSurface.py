#!/usr/bin/python

import string, sys, re, os
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from surface_routines import *
from Enzyme import *
from Selection import *
from Hbond import *

def main():

	"""
returns buried unsatisfied hydrogen bonds
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-c", dest="catalytic", help="catalytic")
	parser.add_option("-x", dest="cutoff", help="surface cutoff", default=3.0)
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

	if not options.selection and not options.catalytic:
		parser.print_help()
		sys.exit()
	

	sasafile = Molecule()
	sele = Selection()
	if options.selection:
		sele.makeSelection(options.selection)

	enz = Enzyme()
	HBN = HBnetwork()
		
	outbase = "clean"
	outpdb  = outbase + ".asa"
	for pdbfile in pdbfiles:
	
		enz.readPDB(pdbfile)
		if options.catalytic:
			icat = int(options.catalytic) - 1
			cres = int(enz.catalytic[icat].file_id)
			newsele = "resi=" + str(cres)
			if options.selection:
				newsele += ";" + options.selection
			sele.clear()
			sele.makeSelection(newsele)
			
		get_surface_area(pdbfile, outbase)
		sasafile.readPDB(outpdb)
		atmlist = sele.apply_selection(sasafile).atomList()

		# return atoms that are not hbonded
		HBN.createNetwork(enz)
		HBN.findHbonds()

		for atm in atmlist:
			found = False
			for hb in HBN.hbonds:
				if atm.name == hb.donor.D.name and atm.resi == hb.donor.D.resi:
					found = True
					break
				if atm.name == hb.donor.H.name and atm.resi == hb.donor.H.resi:
					found = True
					break
				if atm.name == hb.acceptor.A.name and atm.resi == hb.acceptor.A.resi:
					found = True
					break
				if atm.name == hb.acceptor.AA.name and atm.resi == hb.acceptor.AA.resi:
					found = True
					break

			if not found:
				if atm.occupancy < float(options.cutoff):
					print pdbfile + ":",atm
			
		sasafile.clear()
		enz.clear()
		HBN.clear()
		



if __name__ == "__main__":
	main()

