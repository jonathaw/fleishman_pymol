#!/usr/bin/python

from optparse import OptionParser
import os, sys, string, re, commands

def main():

	"""
	saves list of best files based on column info
	"""
	
	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-o", dest="outfile",  help="outfile")
	parser.add_option("-c", dest="col",  help="value column")
	parser.add_option("-u", dest="uniq", help="unique column")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if options.file:
		try:
			FILE = open(options.file)
		except:
			print "unable to open file:",options.file
			sys.exit()
	else:
		parser.print_help()
		sys.exit()

	
	if options.outfile:
		try:
			OUTFILE = open(options.outfile, 'w')
		except:
			print "unable to create outfile:",options.outfile
			sys.exit()
	else:
		parser.print_help()
		sys.exit()

	if not options.col or not options.uniq:
		parser.print_help()
		sys.exit()

	col  = int(options.col)-1
	uniq = int(options.uniq)-1

	scores = []
	id = []
	min_id = ""
	min_score = 9999
	prev_ucol = ""
	for line in FILE.readlines():
		cols = line.split()
		icol = float(cols[col])
		ucol = cols[uniq]

		if ucol == prev_ucol:
			if icol < min_score:
				min_score = icol
				min_id = ucol
				min_line = line
		else:
			if min_id != "":
				OUTFILE.write(min_line)

			prev_ucol = ucol
			min_id = ucol
			min_score = icol
			min_line = line

	OUTFILE.write(min_line)




if __name__ == "__main__":
	main()
