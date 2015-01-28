#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from file_routines import *

def main():

	"""
reports pdbfiles that have a given chain break score
	"""

	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-x", dest="cutoff", help="cutoff", default=3.5)
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true")
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

	cutoff = float(options.cutoff)
	mybreak = re.compile("CHAINBREAK_CST")

	for file in pdbfiles:
		try:
			MYFILE = open(file)
		except:
			print "unable to open file:",file
			sys.exit()

		for line in MYFILE.readlines():
			if mybreak.search(line):
				cols = line.split()
				break_score = float(cols[61])
				if break_score > cutoff:
					if not options.inverse:
						print file,break_score
				else:
					if options.inverse:
						print file,break_score
					break

		MYFILE.close()


if __name__ == "__main__":
	main()
