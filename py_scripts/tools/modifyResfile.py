#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from file_routines import *
from Resfile import *

def main():

	"""
modifies a resfile
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="resfile", help="resfile")
	parser.add_option("-a", dest="allow", help="allow")
	parser.add_option("-d", dest="disallow", help="disallow")
	parser.add_option("-m", dest="mutate", help="modified positions (comma delimited)")
	parser.add_option("--nataa", dest="nataa", help="make NATAA", action="store_true")
	parser.add_option("--natro", dest="natro", help="make NATRO", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.resfile:
		parser.print_help()
		sys.exit()

	if not options.mutate:
		parser.print_help()
		sys.exit()

	mutate = options.mutate.split(",")

	myres = Resfile()
	myres.read(options.resfile)

	for mut in mutate:
		imut = int(mut)-1
		if options.allow:
			myres.expandBy(imut,options.allow)
		if options.disallow:
			myres.restrictBy(imut,options.disallow)
		if options.natro:
			myres.fixedRotamer(imut)
		if options.nataa:
			myres.repackOnly(imut)
		

	myres.write(options.resfile)



if __name__ == "__main__":
	main()
