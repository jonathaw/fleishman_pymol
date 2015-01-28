#!/usr/bin/python

import os, sys, string
from optparse import OptionParser

def main():

	"""
checks for unique columns in a file
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-c", dest="column", help="column")
	parser.add_option("-i", dest="inverse",help="inverse", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.file:
		parser.print_help()
		sys.exit()

	nc = 0
	if options.column:
		nc = int(options.column)

	try:
		FILE = open(options.file, 'r')
	except:
		print "unable to open file"
		sys.exit()


	prev = ""
	cols = []
	for line in FILE.readlines():
		line = string.strip(line)
		cols = string.split(line)

		if prev != cols[nc]:
			if not options.inverse:
				print line
		else:
			if options.inverse:
				print line

		prev = cols[nc]



	



if __name__ == "__main__":
	main()
