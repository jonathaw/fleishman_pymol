#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import os, sys, string, commands, re
from optparse import OptionParser
from file_routines import *



def main():

	"""
maps the position of atoms in a cstfile with an occupancy > 0 to a grid point
	"""

	parser = OptionParser()
	parser.add_option("-c", dest="cstfile", help="cstfile")
	parser.add_option("-C", dest="cstlist", help="cstlist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace",action="store_true")
	parser.add_option("-s", dest="scale",   help="scale", default=0.5)
	parser.add_option("-i", dest="indi", help="individual cst's to scale (comma delimited)")

	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	cstfiles = []
	if options.cstlist:
		cstfiles = files_from_list(options.cstlist)
	elif options.cstfile:
		cstfiles.append(options.cstfile)
	else:
		parser.print_help()
		sys.exit()

	outfiles = []
	if options.outlist:
		outfiles = files_from_list(options.outlist)
	elif options.outfile:
		outfiles.append(options.outfile)
	elif options.replace:
		for file in cstfiles:
			outfiles.append(file)
	else:
		parser.print_help()
		sys.exit()

	if len(cstfiles) != len(outfiles):
		print "number of cstfiles and output files differ"
		sys.exit()

	constraint = re.compile("CONSTRAINT")
	start = re.compile("CST::BEGIN")

	scale = float(options.scale)
	mycst = []
	if options.indi:
		tmp = options.indi.split(",")
		for i in tmp:
			mycst.append(int(i))

	for i in range(len(cstfiles)):
		cstfile = cstfiles[i]
		outfile = outfiles[i]
		try:
			CST = open(cstfile)
		except:
			print "unable to open constraint file"
			sys.exit()


		cstlines = CST.readlines()
		CST.close()

		try:
			OUT = open(outfile, 'w')
		except:
			print "unable to create new file"
			sys.exit()

		ncst = 0
		bchange = True
		for line in cstlines:
			line = string.rstrip(line)
			newline = line
			if start.search(line):
				ncst += 1

			if len(mycst) != 0:
				if ncst in mycst:
					bchange = True
				else:
					bchange = False
	
			if constraint.search(line):
				if bchange:
					cols = line.split()
					val = float(cols[4])
					newval = val*scale
					cols[4] = str(newval)
					newline = ""
					for col in cols:
						newline += col + " "

			OUT.write(newline+"\n")

		OUT.close()




if __name__ == "__main__":
	main()
