#!/usr/bin/python

import string, sys
from optparse import OptionParser
from InteractionGraph import *
from pdb_routines import *

def main():

	"""
	reads in and filters an InteractionGraph
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-e", dest="energy", help="energy")
	parser.add_option("-v", dest="value", help="value")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-t", dest="type", help="type", default="both")
	parser.add_option("-c", dest="clean", help="clean", action="store_true")
	parser.add_option("--res1", dest="res1", help="res1")
	parser.add_option("--res2", dest="res2", help="res2")
	parser.add_option("-b", dest="buried", help="buried")
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true" )
	parser.add_option("-r", dest="resfile", help="resfile")
	parser.add_option("-s", dest="summary", help="summary", action="store_true")
	parser.add_option("-k", dest="keep", help="keep of type")
	parser.add_option("-a", dest="aafilter", help="aafilter",action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file:
		parser.print_help()
		sys.exit()

	if not options.outfile and not options.summary:
		parser.print_help()
		sys.exit()
	
	if options.clean or options.summary or options.keep:
		pass
	elif options.buried:
		if not options.value:
			parser.print_help()
			sys.exit()
	elif options.resfile:
		pass
	elif options.aafilter:
		if not options.res1 or not options.res2:
			parser.print_help()
			sys.exit()
	else:
#		if not options.res1 or not options.res2:
		if not options.energy or not options.value:
			parser.print_help()
			sys.exit()


		
	use_one = False
	use_two = False
	if options.type:
		if options.type == "one":
			use_one = True
		elif options.type == "two":
			use_two = True
		elif options.type == "both":
			use_one = True
			use_two = True
		else:
			print "unrecognized type"
			sys.exit()


	IG = InteractionGraph()
	IG.read(options.file)
	print "before:"
	IG.printStats()
	if (options.summary):
		sys.exit()

	print ""
	
	if options.resfile:
		IG.filter_resfile(options.resfile)
	elif options.buried:
		IG.filter_neighbors(options.buried, float(options.value), options.inverse)
	elif options.clean:
		IG.clean()
	elif options.keep:
		itype = num_from_aa1(options.keep)
		IG.filter_kind(itype,options.inverse)
	elif options.aafilter:
		r1 = num_from_aa1(options.res1)
		r2 = num_from_aa1(options.res2)
		IG.filter_aatypes(r1, r2, options.inverse)
	else:
		r1 = 0
		r2 = 0
		if options.res1:
			r1 = num_from_aa1(options.res1)
		if options.res2:
			r2 = num_from_aa1(options.res2)
		IG.filter_energy(options.energy, options.value, bOne=use_one, bTwo=use_two, type1=r1, type2=r2)

	IG.clean()
	print "ending ..."
	IG.printStats()
	IG.write(options.outfile)


if __name__ == "__main__":
	main()
