#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from InteractionGraph import *

def main():

	"""
This script reports the interactions of a given rotamer with other rotamers using the
two-body energy table
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-r", dest="rotamer_index",help="rotamer index")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file or not options.rotamer_index:
		parser.print_help()
		sys.exit()
	
	IG = InteractionGraph()
	IG.read(options.file)

	rotindex = int(options.rotamer_index)
	rotlist = IG.get_rotamer_partners(rotindex)
	for rot in rotlist:
		myrot = IG.get_rotamer(rot)
		print myrot.index,myrot.seqpos
	


if __name__ == "__main__":
	main()
