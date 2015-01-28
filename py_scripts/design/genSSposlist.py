#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Enzyme import *
from Resfile import *
from file_routines import *
from mol_routines import *
from ss_routines import *

def main():

	"""
creates a resfile from an enzyme.  Redesigned positions are chosen based on their
distance from the ligand and catalytic residues.
By default GLY and PRO positions are unaltered
	"""

	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-a", dest="auto",    help="auto_posfile", action="store_true")
	parser.add_option("--verbose",           dest="verbose", help="verbose", action="store_true")
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

	outfiles = []
	if options.outlist:
		outfiles = files_from_list(options.outlist)
	elif options.outfile:
		outfiles.append(options.outfile)
	elif options.auto:
		for file in pdbfiles:
			base = get_basefile(file)
			file2 = base + ".resfile"
			outfiles.append(file2)
	else:
		parser.print_help()
		sys.exit()

	nfiles = len(pdbfiles)
	if len(outfiles) != nfiles:
		print "number of files differ"
		parser.print_help()
		sys.exit()
		
	
	enz = Enzyme()
	for ifile in range(nfiles):
		enz.clear()

		print pdbfiles[ifile]

		enz.readPDB(pdbfiles[ifile])
		
		# get secondary structure 
		natss = getSecondaryStructure(pdbfiles[ifile])

		prot = enz.protein	
		lig  = enz.ligand
		nres = len(prot.residue)

		designable = [False]*nres
		repackable = [False]*nres
		FILE0 = open(outfiles[ifile], 'w')

		for i in range(nres):
			res = prot.residue[i]
			CB = None
			if res.name == "GLY":
					CB = res.getAtom(" CA ")
			else:
					CB = res.getAtom(" CB ")

			if CB == None:
				continue

		# --- get distance to ligand --- #
			distCB = closestApproachToResidue(CB,lig)					
			if distCB < 9.0:
				designable[i] = True
			elif distCB < 11.0:
				if isResPointingToRes(res, lig, cutoff=60):
					designable[i] = True
			if designable[i]:
				#if natss[i] == "H" and natss[i+2] == "H" and natss[i+4] == "H":
				FILE0.write(str(i) + " ") 
		

		FILE0.write("\n")
                FILE0.close()

if __name__ == "__main__":
	main()
