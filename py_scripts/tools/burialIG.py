#!/usr/bin/python

import string, sys
from optparse import OptionParser
from InteractionGraph import *
from pdb_routines import *

def main():

	"""
	filters so that the number of neighbors of residue 1 > residue 2
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("--res1", dest="res1", help="res1")
	parser.add_option("--res2", dest="res2", help="res2")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file or not options.outfile:
		parser.print_help()
		sys.exit()

	if not options.res1 or not options.res2:
		parser.print_help()
		sys.exit()

	r1 = num_from_aa1(options.res1)
	r2 = num_from_aa1(options.res2)

	IG = InteractionGraph()
	IG.read(options.file)
	print "before:"
	IG.printStats()

	cpedge = []
	for edge in IG.edges:
		rot1 = IG.get_rotamer(edge.rotindex1)
		rot2 = IG.get_rotamer(edge.rotindex2)

		if rot1.aatype == r1 and rot2.aatype == r2:
			orot1 = rot1
			orot2 = rot2
		elif rot1.aatype == r2 and rot2.aatype == r1:
			orot1 = rot2
			orot2 = rot1
		else:
			# only filter residues we're interest in
			cpedge.append(edge)
			continue

		pos1 = orot1.seqpos
		pos2 = orot2.seqpos

		if IG.neighbors[pos1] > IG.neighbors[pos2]:
			cpedge.append(edge)

	IG.edges = cpedge
	IG.clean()

	print "ending ..."
	IG.printStats()
	IG.write(options.outfile)



if __name__ == "__main__":
	main()
