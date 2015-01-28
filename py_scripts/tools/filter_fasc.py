#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from optparse import OptionParser
import sys, os, string


def main():

	"""
filters fasc files
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="fasc_file", help="fasc file")
	parser.add_option("-s", dest="summary", help="print energy columns", action="store_true")
	parser.add_option("-e", dest="energy", help="energy")
	parser.add_option("-x", dest="cutoff", help="cutoff")
	parser.add_option("-p", dest="print_value", help="print values", action="store_true")
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.fasc_file:
		parser.print_help()
		sys.exit()

	try:
		FASC = open(options.fasc_file)
	except:
		print "unable to open fasc file"
		sys.exit()

	lines = FASC.readlines()
	cols = lines[0].split()
	fasc_info = []
	fasc_header = []

	if options.summary:
		for col in cols:
			print col
		return

	if not options.energy:
		parser.print_help()
		return

	if not options.cutoff and not options.print_value:
		parser.print_help()
		return

	if not options.energy in cols:
		print "cannot find energy term",options.energy
		print "usage -s (summary) to see available energy terms"
		return 


	for col in cols:
		ene = []
		fasc_header.append(col)
		fasc_info.append(ene)
	
	ihead = -1
	nhead = 0
	for head in fasc_header:
		if head == options.energy:
			ihead = nhead
		nhead += 1

	nlines = len(lines)
	nvalues = nlines -1
	for iline in range(1,nlines):
		line = lines[iline]
		cols = line.split()	
		ncol = 0
		for col in cols:
			fasc_info[ncol].append(col)
			ncol += 1

	if options.print_value:
		for i in range(nvalues):
			print fasc_info[0][i],fasc_info[ihead][i]

	if options.cutoff:
		cutoff = float(options.cutoff)
		for i in range(nvalues):
			keep = False
			if float(fasc_info[ihead][i]) < cutoff:
				keep = True

			if options.inverse:
				if not keep:
					print fasc_info[0][i],fasc_info[ihead][i]
			else:
				if keep:
					print fasc_info[0][i],fasc_info[ihead][i]
					
	

if __name__ == '__main__':
	main()
