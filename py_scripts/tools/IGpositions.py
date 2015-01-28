#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from InteractionGraph import *
from pdb_routines import *

def main():

	"""
lists the positions for a residue type in the interaction graph
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-a", dest="aatype", help="aatype")
	parser.add_option("-p", dest="pymol_format", help="pymol format", action="store_true")
	parser.add_option("-o", dest="posfile", help="posfile")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file or not options.aatype:
		parser.print_help()
		sys.exit()
	
	IG = InteractionGraph()
	IG.read(options.file)

	ntype = num_from_aa1(options.aatype)

	positions = []
	for rot in IG.rotamers:
		if rot.aatype == ntype:
			if not rot.seqpos in positions:
				positions.append(rot.seqpos)
	
	if options.pymol_format:
		out = "(resi "
		for pos in positions:
			if pos == positions[-1]:
				out += str(pos) + ")"
			else:
				out += str(pos) + ","

		print out
	elif options.posfile:
		try:
			POS = open(options.posfile, 'w')
		except:
			print "unable to create new posfile"
			sys.exit()
		out = ""
		for pos in positions:
			out += str(pos) + " "
		POS.write(out + "\n")
	else:
		for pos in positions:
			print pos


if __name__ == "__main__":
	main()
