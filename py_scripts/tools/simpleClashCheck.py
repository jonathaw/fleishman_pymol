#!/usr/bin/python


from Enzyme import *
from Selection import *
from optparse import OptionParser
import os, sys, string, re
from mol_routines import *
from file_routines import *



def main():

	"""
	performs a simple clash check (hard spheres)
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="scale", help="scale (0.60)", default=0.60)
	parser.add_option("-S", dest="sele", help="selection")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdbfile:
		pdbfiles.append(options.pdbfile)
	elif options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	else:
		parser.print_help()
		sys.exit()

	myscale = float(options.scale)	
	mymol = Enzyme()

	sele = None
	if options.sele:
		sele = Selection()
		sele.makeSelection(options.sele)

	for pdbfile in pdbfiles:
		mymol.readPDB(pdbfile)
		if options.sele:
			reslist = sele.apply_selection(mymol).residueList()
		else:
			reslist = mymol.residueList()

		nres = len(reslist)
		bFail = False
		for i in range(nres):
			for j in range(i+1,nres):
				if (bResidue_Residue_clash_check(reslist[i], reslist[j], myscale)):
					print pdbfile,reslist[i].file_id,reslist[j].file_id,"FAIL"
					bFail = True
					break

			if bFail:
				break

		
		mymol.clear()



if __name__ == "__main__":
	main()

