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
forces hydrophobic mutation
NOTE: FOR NOW DOESN'T ALLOW R OR A
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-l", dest="list", help="list mutations", action="store_true")
	parser.add_option("-s", dest="summary", help="summary", action="store_true")
	parser.add_option("-d", dest="dry_run", help="dry_run", action="store_true")
	parser.add_option("-R", dest="charged", help="charged only", action="store_true")
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

	protein = Enzyme()
	for pdbfile in pdbfiles:
		npol_run = "contactingPolars.py -s 'resn=LG1;element!=V' --ignore_catalytic -p " + pdbfile
		if options.charged:
			npol_run += " -R"
		pol_run  = "contactingPolars.py -s 'resn=LG1;name=OH  ,Nhis,OOC ,OCbb,COO ' --ignore_catalytic -p " + pdbfile
		if options.charged:
			pol_run += " -R"
		np = commands.getoutput(npol_run)
		pl = commands.getoutput(pol_run)

		npol = np.split("\n")
		pol  = pl.split("\n")

		mutate = []
		for line in npol:
			if not (line in pol):
				cols = line.split()
				if not (int(cols[0]) in mutate):
					mutate.append(int(cols[0]))

		protein.readPDB(pdbfile)

		toMutate = -1
		maxhb = -999
		for mut in mutate:
			myres = protein.getResidue(mut)
			if myres == None:
				print "cannot find residue"
				sys.exit()

			if myres.EhbSC > maxhb:
				maxhb = myres.EhbSC
				toMutate = mut

		protein.clear()
		if options.summary:
			print pdbfile,len(mutate)
			continue

		if options.list:
			for mut in mutate:
				print pdbfile,mut

		if options.dry_run:
			if toMutate > -1:
				print pdbfile,toMutate
			else:
				print pdbfile,"none"
			continue

		mut_run = "ligandResfile.py -p " + pdbfile + " -a --keep_nonpolar --no_non_native='AR' --force_hydrophobic " + str(toMutate)
		commands.getoutput(mut_run)


if __name__ == "__main__":
	main()

