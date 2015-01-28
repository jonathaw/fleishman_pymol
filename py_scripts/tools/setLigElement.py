#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import sys, os, string
from optparse import OptionParser
from file_routines import *


def main():

	"""
sets the appropriate element for atoms in a ligand.  (uses known rosetta
atomtypes)
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	if not options.replace:
		parser.print_help()
		sys.exit()

	outfiles = []
	for file in pdbfiles:
		outfiles.append(file)

	het = re.compile("HETATM")

	for i in range(len(pdbfiles)):
		try:
			PDBFILE = open(pdbfiles[i])
		except:
			print "can't open pdbfile"
			sys.exit()

		mylines = PDBFILE.readlines()
		PDBFILE.close()

		try:
			OUTFILE = open(pdbfiles[i],'w')
		except:
			print "can't write to outfile"
			sys.exit()

		nat = 9000
		for line in mylines:
			newline = line
			if het.match(line):
				if line[12:16] == "CH1 ":
					newline = line[0:66] + "           C" + "\n"
				if line[12:16] == "Nhis":
					newline = line[0:66] + "           N" + "\n"
				if line[12:16] == "OOC ":
					newline = line[0:66] + "           O" + "\n"
				if line[12:16] == "aroC":
					newline = line[0:66] + "           C" + "\n"
				if line[12:16] == "OH  ":
					newline = line[0:66] + "           O" + "\n"
				if line[12:16] == "COO ":
					newline = line[0:66] + "           C" + "\n"
				if line[12:16] == "Haro":
					newline = line[0:66] + "           H" + "\n"
				if line[12:16] == "Hapo":
					newline = line[0:66] + "           H" + "\n"
				if line[12:16] == "Hpol":
					newline = line[0:66] + "           H" + "\n"

			OUTFILE.write(newline)

		OUTFILE.close()


				






if __name__ == "__main__":
	main()
