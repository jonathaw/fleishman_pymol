#!/usr/bin/python

import string, sys, re, os, commands
from optparse import OptionParser
from file_routines import *

def main():

	"""
	makes sure that asp or glu have 2 hbonds
	"""

	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-x", dest="cutoff", help="cutoff", default=-0.3)
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.pdblist:
		parser.print_help()
		sys.exit()

	pdbfiles = []
	pdbfiles = files_from_list(options.pdblist)

	for file in pdbfiles:
		exe = "checkHbonds.py -p " + file + " -x " + str(options.cutoff)
		ans = commands.getoutput(exe)
		lines = ans.split("\n")

		OD1found = False
		OD2found = False
		OE1found = False
		OE2found = False

		donor =  ""
		acceptor = ""
		exe = ""

			
		for line in lines:
			cols = line.split()
			if len(cols) < 8:
				continue

			found = False
			if cols[1] == "SER":
				if cols[3] == "OG":
					if cols[8] == "OD1":
						OD1found = True
						found = True
					if cols[8] == "OD2":
						OD2found = True
						found = True
					if cols[8] == "OE1":
						OE1found = True
						found = True
					if cols[8] == "OE2":
						OE2found = True
						found = True
			if cols[1] == "THR":
				if cols[3] == "OG1":
					if cols[8] == "OD1":
						OD1found = True
						found = True
					if cols[8] == "OD2":
						OD2found = True
						found = True
					if cols[8] == "OE1":
						OE1found = True
						found = True
					if cols[8] == "OE2":
						OE2found = True
						found = True

			if found:
				donor = "resi=" + cols[2]
				if OD1found:
					acceptor = "name= OD1"
				if OD2found:
					acceptor = "name= OD2"
				if OE1found:
					acceptor = "name= OE1"
				if OE2found:
					acceptor = "name= OE2"

				exe = "pointHbonds.py -p " + file + " -r -d '" + donor + "' -a '" + acceptor + "'"


		if exe != "":
			ans = commands.getoutput(exe)





if __name__ == "__main__":
	main()
