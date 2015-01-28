#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from Resfile import *
from file_routines import *

def main():

	"""
creates a template resfile from a given pdbfile.  The user can specify which types of
residues to allow at each position
	"""

	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-a", dest="auto",    help="auto resfile", action="store_true")
	parser.add_option("-r", dest="residues", help="residues")
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


	Protein = Molecule()
	resfile = Resfile()
	for ifile in range(nfiles):
		Protein.clear()
		resfile.clear()

		Protein.readPDB(pdbfiles[ifile])
		resfile.setMolecule(Protein)

		if options.residues:
			nres = Protein.chain[0].numResidues()
			for i in range(nres):
				resfile.designResidue(i,options.residues)

		resfile.write(outfiles[ifile])	



if __name__ == "__main__":
	main()
