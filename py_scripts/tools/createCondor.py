#!/usr/bin/python

import string, sys, re, os
from optparse import OptionParser

def main():

	"""
creates a pbs file to execute a given command
	"""

	parser = OptionParser()
	parser.add_option("-e", dest="executable", help="executable")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.executable or not options.outfile:
		parser.print_help()
		sys.exit()

	try:
		PBS = open(options.outfile, 'w')
	except:
		print "cannot open ",options.outfile
		sys.exit()

	PBS.write("universe = vanilla\n")
	PBS.write("executable = " + options.executable + "\n")
	PBS.write("log = condor.log\n")
	PBS.write("getenv = TRUE\n")
	PBS.write("output = condor.output\n")
	PBS.write("queue\n")

	PBS.close()



if __name__ == "__main__":
	main()
