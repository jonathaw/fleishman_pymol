#!/usr/bin/python

from Molecule import *
from Selection import *
from optparse import OptionParser
from file_routines import *
import sys, string, re


def main():

	"""
changes the older matching header information to the new constraint header
(HETATMS are changed to LG1)
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
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


	match_head = re.compile("REMARK BACKBONE TEMPLATE A")
	het        = re.compile("HETATM")
	new_lig    = "LG1"
	for pdbfile in pdbfiles:
		try:
			PDB = open(pdbfile)
		except:
			print "unable to open pdbfile:",pdbfile
			sys.exit()

		outfile = []
		for line in PDB.readlines():
			line = string.rstrip(line)
			newline = line
			if match_head.match(line):
				cols = line.split()
				resn = cols[4]
				resi = int(cols[5])
				cati = int(cols[11])
				newline = ("REMARK BACKBONE TEMPLATE A LG1    0 MATCH MOTIF B %3s%6i%3i"%(resn,resi,cati))

			if het.match(line):
				old_lig = line[17:20]
				newline = line.replace(old_lig,new_lig)

			outfile.append(newline)

		PDB.close()
		try:
			PDB = open(pdbfile, 'w')
		except:
			print "unable to create pdbfile:",pdbfile
			sys.exit()

		for line in outfile:
			PDB.write(line + "\n")
		PDB.close()
			
		


if __name__ == "__main__":
	main()

