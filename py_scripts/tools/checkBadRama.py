#!/usr/bin/python

import sys, os, string,re
from optparse import OptionParser
from file_routines import *
from Molecule import *



def main():

	"""
reports the number of residues in a pdbfile
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-x", dest="cutoff", help="cutoff",default=3.0)
	parser.add_option("-n", dest="native", help="native")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()	


	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	if not options.cutoff:
		parser.print_help()
		sys.exit()

	nat_mol = None
	if options.native:
		nat_mol = Molecule()
		nat_mol.readPDB(options.native)
		nat_seq = nat_mol.sequence()
		

	re_complete = re.compile("complete")
	rama_cutoff = float(options.cutoff)
	for pdbfile in pdbfiles:
		try:
			PDB = open(pdbfile)
		except:
			print "unable to open pdbfile"
			sys.exit()

		bRead = False
		for line in PDB.readlines():
			if re_complete.match(line):
				bRead = True
				continue

			if bRead:
				cols = line.split()
				if len(cols) < 10:
					bRead = False
					continue

				eRama = float(cols[6])
				if eRama > rama_cutoff:
					if options.native:
						print pdbfile,cols[0],cols[7],eRama,nat_seq[int(cols[0])-1]
					else:
						print pdbfile,cols[0],cols[7],eRama




if __name__ == "__main__":
	main()

	
