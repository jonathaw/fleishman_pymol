#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Enzyme import *
from Selection import *

def main():

	"""
adds a centroid
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-t", dest="type", help="atom type", default="CS1 ")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-w", dest="wobble", help="wobble", action="store_true")
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
	elif options.replace:
		for file in pdbfiles:
			outfiles.append(file)
	else:
		parser.print_help()
		sys.exit()

	nfiles = len(pdbfiles)
	if nfiles != len(outfiles):
		print "number of input and output files differ"
		sys.exit()

	if not options.selection:
		parser.print_help()
		sys.exit()

	mymol = Enzyme()
	sele  = Selection()
	sele.makeSelection(options.selection)
	for i in range(nfiles):
		pdbfile = pdbfiles[i]
		outfile = outfiles[i]

		mymol.readPDB(pdbfile)
		alist = sele.apply_selection(mymol).atomList()

		if len(alist) == 0:
			print "pdbfile: no atoms"
			continue

		com = vector3d()		
		for atm in alist:
			com += atm.coord

		com /= float(len(alist))

		newatm = mymol.ligand.newAtom()
		newatm.name = options.type
		newatm.coord.x = com.x
		newatm.coord.y = com.y
		newatm.coord.z = com.z
		newatm.kind    = "HETATM"
		if options.wobble:
			newatm.coord.x += 0.001
			newatm.coord.y -= 0.001
			newatm.coord.z += 0.001

		mymol.writePDB(outfile)
		mymol.clear()


if __name__ == "__main__":
	main()
