#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from InteractionGraph import *
from pdb_routines import *

def main():

	"""
	creates a rosetta pos file from an IG
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file:
		parser.print_help()
		sys.exit()
	
	IG = InteractionGraph()
	IG.read(options.file)


	pos_data = {}
	for rot in IG.rotamers:
		seqpos = rot.seqpos
		aatype = rot.aatype

		if not pos_data.has_key(aatype):
			pos_data[aatype] = {}

		pos_data[aatype][seqpos] = True

	for key in pos_data.keys():
		outfile = "posfile_" + aa3_from_num(key)

		print outfile
		try:
			OUTPUT = open(outfile, 'w')
		except:
			print "unable to open outfile"
			sys.exit()

		mylist = pos_data[key].keys()
		mylist.sort()
		for seqpos in mylist:
		#for seqpos in pos_data[key].keys():
			OUTPUT.write(str(seqpos) + " ")

		OUTPUT.write("\n")
		OUTPUT.close()

	
		


if __name__ == "__main__":
	main()
