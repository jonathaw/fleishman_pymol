#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from file_routines import *


def main():

	"""
	shows the clashes found in a rosetta pdbfile
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-c", dest="cutoff",  help="cutoff", default=1.5)
	parser.add_option("-v", dest="verbose", help="verbose", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()


	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	startline = re.compile("res aa    Eatr")
	endline = re.compile("totals")

	if options.outfile:
		try:
			OUTFILE = open(options.outfile, 'w')
		except:
			print "unable to create outfile"
			sys.exit()

	for pdbfile in pdbfiles:
		first = False
		try:
			FILE = open(pdbfile)
		except:
			print "unable to open pdbfile"
			sys.exit()



		bRead = False
		for line in FILE.readlines():
			line = string.rstrip(line)

			if startline.match(line):
				bRead = True
				continue

			if bRead and endline.match(line):
				bRead = False

			if bRead:
				cols = line.split()
				Erep = float(cols[3])

				if Erep > float(options.cutoff):
					#if cols[1] == "CYS":
					#	continue

					if options.outfile:
						if not first:
							OUTFILE.write(pdbfile + ":\n")
						OUTFILE.write(cols[0] + "\n")
					if options.verbose:
						if not first:
							print pdbfile + ":"
						print "   ",cols[0],cols[1],Erep
					else:
						if not first:
							print pdbfile

					first = True

	if options.outfile:
		OUTFILE.close()
		
		
	
if __name__ == "__main__":
	main()
