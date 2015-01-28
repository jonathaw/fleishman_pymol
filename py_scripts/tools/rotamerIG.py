#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from InteractionGraph import *
from pdb_routines import *

def main():

	"""
	filters an interaction graph to only contain a given rotamer list
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-l", dest="list", help="list")
	parser.add_option("-g", dest="log",  help="log")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-a", dest="aatype", help="aatype")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file:
		parser.print_help()
		sys.exit()

	if options.outfile:
		outfile = options.outfile
	elif options.replace:
		outfile = options.file
	else:
		parser.print_help()
		sys.exit()

	if not options.aatype:
		parser.print_help()
		sys.exit()

	rotlist = []
	if options.list:
		try:
			LIST = open(options.list)
		except:
			print "unable to open list"
			sys.exit()

		for line in LIST.readlines():
			rline = string.rstrip(line)
			rot_index = int(rline)
			rotlist.append(rot_index)
		LIST.close()
	elif options.log:
		try:
			LOG = open(options.log)
		except:
			print "unable to open log"
			sys.exit()	

		restring = re.compile("InteractionGraph")
		for line in LOG:
			if restring.match(line):
				cols = line.split()
				rot_index = int(cols[3])	
				
				if not rot_index in rotlist:
					rotlist.append(rot_index)
	else:
		parser.print_help()
		sys.exit()

	
	iaa = num_from_aa1(options.aatype)
	IG = InteractionGraph()
	IG.read(options.file)
	print "starting ..."
	IG.printStats()
	IG.keepRotamerList(iaa,rotlist)
	IG.clean()
	print ""
	print "ending ..."
	IG.printStats()
	IG.write(outfile)


if __name__ == "__main__":
	main()
