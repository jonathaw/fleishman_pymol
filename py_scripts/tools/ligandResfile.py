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
	creates a resfile from an enzyme
	"""

	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("--no_gly", dest="no_gly", help="no glycine at ss", action="store_true")
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
	else:
		parser.print_help()
		sys.exit()

	nfiles = len(pdbfiles)
	if len(outfiles) != nfiles:
		print "number of files differ"
		parser.print_help()
		sys.exit()
		
	
	enz = Enzyme()
	resfile = Resfile()
	for ifile in range(nfiles):
		enz.clear()
		resfile.clear()

		enz.readPDB(pdbfiles[ifile])
		resfile.setMolecule(enz)

		if options.no_gly:
			natss = getSecondaryStructure(pdbfiles[ifile])
			if len(natss) < enz.protein.numResidues():
				print "number of residues and secondary structure do no match"
				sys.exit()


		prot = enz.protein	
		lig  = enz.ligand
		nres = len(prot.residue)

		designable = [False]*nres
		repackable = [False]*nres
		for i in range(nres):
			res = prot.residue[i]
			if enz.isCatalytic(res):
				resfile.setCatalytic(i)
			else:
				if res.name == "GLY":
					CB = res.getAtom(" CA ")
				else:
					CB = res.getAtom(" CB ")

				#if options.only_cat:
				# --- get distance to ligand --- #
				distCB = closestApproachToResidue(CB,lig)
				if distCB < 6.0:
					designable[i] = True
				elif distCB < 8.0:
					if isResPointingToRes(res, lig, cutoff=60):
						designable[i] = True
					else:
						repackable[i] = True
				elif distCB < 10.0:
					repackable[i] = True

				
				# --- get distance to residue 
				focusedRes = None
				mindist = 5000
				for cres in enz.catalytic:
					dist = closestApproachToResidue(CB, cres)
					if dist < mindist:
						focusedRes = cres
						mindist = dist

				if focusedRes != None:
					if mindist < 5.5:
						if isResPointingToRes(res, focusedRes, cutoff=60):
							designable[i] = True
						else:
							repackable[i] = True
					elif mindist < 7.0:
						repackable[i] = True


		for i in range(nres):
			res = enz.protein.residue[i]
			if designable[i]:
				if options.no_gly and res.name != "GLY":
					if natss[i] == "H" or natss[i] == "E":
						resfile.designNoGly(i)
					else:
						resfile.designOnly(i)
				else:
					resfile.designOnly(i)
			elif repackable[i]:
				resfile.repackOnly(i)
					
						
		resfile.write(outfiles[ifile])




if __name__ == "__main__":
	main()
