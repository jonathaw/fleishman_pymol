#!/usr/bin/python

import string, sys, re, commands
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Enzyme import *

def main():

	"""
detects duplicate matches by using md5sum on a set of reduced precision pdbfiles
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
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
	mdexe = ""
	mycol = 0
	if exe_present("md5"):
		mdexe = "md5"
		mycol = 3
	elif exe_present("md5sum"):
		mdexe = "md5sum"
		mycol = 0

	tmpfile = "_dup_.pdb"
	commands.getoutput("rm -f " + tmpfile)
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		if protein.numResidues() == 0:
			continue

		reducePDBprecision(protein)
		protein.writePDB(tmpfile)

		mycmd = mdexe + " " + tmpfile
		output = commands.getoutput(mycmd)
		cols = output.split()
		myvar = cols[mycol]
		print pdbfile,myvar

		# safety net
		commands.getoutput("rm -f " + tmpfile)

		protein.clear()

		



if __name__ == "__main__":
	main()
