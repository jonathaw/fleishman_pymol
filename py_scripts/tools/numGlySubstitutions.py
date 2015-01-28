#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from file_routines import *
from ss_routines import *
from Enzyme import *

def main():

	"""
reports the number of glycine substitutions in a designed sequence
reports total gylcine substituions and number of glycines in secondary structure
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-n", dest="native",  help="native")
	parser.add_option("-f", dest="force", help="force alignment", action="store_true")
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

	if not options.native:
		parser.print_help()
		sys.exit()

	enz = Enzyme()
	nat = Enzyme()
	nat.readPDB(options.native)
	natss   = getSecondaryStructure(options.native)
	natseq  = nat.protein.sequence()

	if not options.force:
		if natss != "" and (len(natss) != len(natseq)):
			print natss
			print natseq
			print "PROBLEM WITH NATSS"
			sys.exit()

	for pdbfile in pdbfiles:
		n_gly_ss  = 0
		n_gly_tot = 0
		enz.readPDB(pdbfile)

		myseq = enz.protein.sequence()	

		mismatch = []
		mysize = len(natseq)
		if len(myseq) != len(natseq):
			if options.force:
				mysize = min(len(myseq),len(natseq))
			else:
				print "sequence lengths differ"
				print "you can try the -force option"
				sys.exit()

		for i in range(mysize):
			if myseq[i] != natseq[i]:

				if myseq[i] == "G" and (natss[i] == "H" or natss[i] == "E"):
					n_gly_ss += 1

				if myseq[i] == "G":
					n_gly_tot += 1
	
		enz.clear()
		print pdbfile,n_gly_tot,n_gly_ss




if __name__ == "__main__":
	main()
