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
	parser.add_option("-n", dest="name", help="name")
	parser.add_option("-t", dest="time", help="time", default="12:00:00")
	parser.add_option("-d", dest="cwd", help="use cwd", action="store_true")
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

	run_name = "run"
	if options.name:
		run_name = options.name
	elif options.cwd:
		tmp = os.getcwd()
		cols = tmp.split("/")
		run_name = "n" + cols[-1]

	PBS.write("#PBS -j oe\n")
	PBS.write("#PBS -N " + run_name + "\n")
	PBS.write("#PBS -l nodes=1:ppn=1\n")
	PBS.write("#PBS -l walltime=" + options.time + "\n")
	PBS.write("\n")
	PBS.write("cd $PBS_O_WORKDIR\n")
	PBS.write("\n")
	PBS.write(options.executable + "\n")

	PBS.close()



if __name__ == "__main__":
	main()
