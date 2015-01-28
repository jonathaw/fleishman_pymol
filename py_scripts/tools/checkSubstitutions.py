#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from file_routines import *
from ss_routines import *
from Enzyme import *
from ResidueProperties import *

def main():

	"""
compares a designed protein's sequence to the native sequence and reports the 
number of mutations
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-n", dest="native",  help="native")
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

	if natss != "" and (len(natss) != len(natseq)):
		print natss
		print natseq
		print "PROBLEM WITH NATSS"
		sys.exit()

	resprop = ResidueProperties()

	for pdbfile in pdbfiles:
		n_gly_ss = 0
		n_np_pol = 0
		n_np_chg = 0

		enz.readPDB(pdbfile)

		catlist = []
		for cres in enz.catalytic:
			catlist.append(int(cres.file_id))

		myseq = enz.protein.sequence()	

		mismatch = []
		if len(myseq) != len(natseq):
			print "sequence lengths differ"
			sys.exit()

		mm_ss = ""
		mm_ns = ""
		mm_ps = ""

		for i in range(len(myseq)):
			if i in catlist:
				continue

			if myseq[i] != natseq[i]:
				mm_ss += natss[i]
				mm_ns += natseq[i]
				mm_ps += myseq[i]

				if myseq[i] == "G" and (natss[i] == "H" or natss[i] == "E"):
					n_gly_ss += 1

				if resprop.isNonPolar(code=natseq[i]) or natseq[i] == "F":
					if resprop.isPolar(code=myseq[i]):
						n_np_pol += 1
					if resprop.isCharged(code=myseq[i]):
						n_np_chg += 1
	
		print mm_ss
		print mm_ns
		print mm_ps

		print pdbfile
		print "# glycines in ss:",n_gly_ss
		print "# np to pol:",n_np_pol
		print "# np to chg:",n_np_chg
		print "--------------"

		enz.clear()




if __name__ == "__main__":
	main()
