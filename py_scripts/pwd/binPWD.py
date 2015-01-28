#!/usr/bin/python


import os, sys, string, commands, re
from optparse import OptionParser
from Molecule import *

def main():
	parser = OptionParser()
	parser.add_option("-p", dest="pwdfile", help="pwdfile")
	parser.add_option("-P", dest="pwdlist", help="pwdlist")
	parser.add_option("-b", dest="bin", help="bin", default=0.5)
	parser.add_option("-c", dest="cutoff", help="cutoff", default=15.0)
	parser.add_option("-s", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile", default="output")
	(options, args) = parser.parse_args()


	pwdfiles = []
	if options.pwdlist:
		try:
			LIST = open(options.pwdlist)
		except:
			print "unable to open pwdlist"
			sys.exit()

		for line in LIST.readlines():
			line = string.rstrip(line)
			pwdfiles.append(line)
	elif options.pwdfile:
		pwdfiles.append(options.pwdfile)
	else:
		parser.print_help()
		sys.exit()
	
	if not options.pdbfile:
		parser.print_help()
		sys.exit()



	protein = Molecule()
	protein.readPDB(options.pdbfile)
	seq = protein.sequence()
	print seq


	try:
		OUTFILE = open(options.outfile, 'w')
	except:
		print "unable to create outfile",options.outfile
		sys.exit()


	inter = re.compile("Inter-residue")
	total = re.compile("Total")

	polars = []
	polars.append("D")
	polars.append("E")
	polars.append("K")
	polars.append("R")


	bRead = False
	out   = []
	for file in pwdfiles:
		print file
		try:
			FILE = open(file, 'r')
		except:
			print "unable to open pwdfile",options.pwdfile
			sys.exit()

		for line in FILE.readlines():
			line = string.rstrip(line)

			if inter.search(line):
				bRead = True

			if bRead and line[0:1] != "#":
				if total.search(line):
					bRead = False
					break

				#print line
				cols = line.split()
				resj = int(cols[0])
				resi = int(cols[1])
				eab  = float(cols[6])
				dist = float(cols[5])

				if dist > options.cutoff:
					if abs(resi-resj) > 2:
						seqi = seq[resi-1:resi]
						seqj = seq[resj-1:resj]

						if not seqi in polars or not seqj in polars:
							continue

						OUTFILE.write(seqi + seqj + " " + str(resi) + " " + str(resj) + " " + str(dist) + " " + str(eab) + "\n")
		FILE.close()

	OUTFILE.close()



if __name__ == "__main__":
	main()
