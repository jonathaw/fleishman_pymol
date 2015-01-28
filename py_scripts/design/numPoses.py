#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import os, sys, string, commands,re
from optparse import OptionParser


def main():

	"""
returns the number of conformations sampled for a given heterofile
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		try:
			LIST = open(options.pdblist, 'r')
		except:
			print "unable to open pdblist"
			sys.exit()

		for line in LIST.readlines():
			line = string.rstrip(line)
			pdbfiles.append(line)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	atm = re.compile("ATOM|HETATM")

	for pdbfile in pdbfiles:
		try:
			FILE = open(pdbfile)
		except:
			print "unable to open pdbfile"
			return

		for line in FILE.readlines():
			line = string.rstrip(line)

			if atm.match(line):	
				length = len(line)
				if length > 120:
					ndist   = float(line[108:114])	
					nang    = float(line[132:138])
					ntor    = float(line[156:162])
					bnang   = float(line[180:186])
					bntor1  = float(line[204:210])
					bntor2  = float(line[228:234])

					ndist = 2*ndist + 1
					nang = 2*nang + 1
					ntor = 2*ntor + 1
					bnang = 2*bnang + 1
					bntor1 = 2*bntor1 + 1
					bntor2 = 2*bntor2 + 1

					n = int(ndist * nang * ntor * bnang * bntor1 * bntor2)
					print line[12:16] + " => " + str(n)

		FILE.close()

if __name__ == "__main__":
	main()
