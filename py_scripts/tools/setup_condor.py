#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string, sys, os, commands
from optparse import OptionParser


def main():

	"""
creates sets of directories and fills them with files from a list
	"""

	parser = OptionParser()
	parser.add_option("-b", dest="binary", help="binary", default="~/bin/trunk.gcc")
	parser.add_option("-a", dest="args", help="arguments")
	parser.add_option("-A", dest="argfile", help="argfile")
	parser.add_option("-n", dest="split", help="numsplit")
	parser.add_option("-l", dest="list", help="list", default="list")
	parser.add_option("-o", dest="output", help="output")
	parser.add_option("-s", dest="syd", help="syd", action="store_true")
	parser.set_description(main.__doc__)


	(options, args) = parser.parse_args()

	if not options.output:
		parser.print_help()
		sys.exit()

	if options.args:
		myargs = options.args
	elif options.argfile:
		try:
			ARGFILE = open(options.argfile)
		except:
			print "unable to open argfile"
			sys.exit()

		myargs = ARGFILE.readline()

	try:
		CONDOR = open(options.output, 'w')
	except:
		print "unable to open condor"
		sys.exit()

	CONDOR.write("#automatically generated condor script\n")
	CONDOR.write("Universe     =   vanilla\n")
	CONDOR.write("Output       =   rosetta.out$(Process)\n")
	CONDOR.write("Error        =   rosetta.err$(Process)\n")
	CONDOR.write("Log          =   condor.log\n")
	CONDOR.write("Getenv       =   True\n")
	CONDOR.write("Notification =   Never\n")

	bin = options.binary
	if "~" in options.binary and options.syd:
		bin = bin.replace("~", "/work1/wollacott")

	CONDOR.write("Executable   =   " + bin + "\n")
	CONDOR.write("Arguments    =   " + myargs + "\n")

	CONDOR.write("mychoice = $RANDOM_CHOICE(1,2)\n")
	if not options.syd:
		CONDOR.write("Initialdir = ./\n")
	else:
		pwd = os.getcwd()
		pwd = pwd.replace("tt/work1", "tt/work$(mychoice)")
		CONDOR.write("Initialdir = " + pwd + "\n")

	exe = "splitList.py -l " + options.list + " -b " + options.split
	#print exe
	nque = commands.getoutput(exe)
	CONDOR.write("Queue " + str(nque) + "\n")
	CONDOR.close()

			

	


if __name__ == "__main__":
	main()
