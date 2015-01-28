#!/usr/bin/python


import os, sys, string
from optparse import OptionParser


def main():

	"""
takes a SORTED list of values and reports the number of each occurance
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-c", dest="column", help="column")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.file or not options.column:
		parser.print_help()
		sys.exit()

	try:
		FILE = open(options.file, 'r')
	except:
		print "unable to open file"
		sys.exit()

	prevline = ""
	nlines   = 0
	nconseq  = 1
	last     = ""
	for line in FILE.readlines():
		line = string.rstrip(line)
		if line != prevline and nlines != 0:
			print prevline,nconseq	
			nconseq = 1
		else:
			nconseq += 1
		
		nlines += 1
		prevline = line

	print prevline,nconseq
	

			

if __name__ == "__main__":
	main()
