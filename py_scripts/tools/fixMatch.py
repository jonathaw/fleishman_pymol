#!/usr/bin/python

from optparse import OptionParser
from file_routines import *
import sys, string


def main():
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
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

	for pdbfile in pdbfiles:
		try:
			pdb = open(pdbfile)
		except:
			print "unable to open pdbfile"
			sys.exit()

		output = []
		for line in pdb.readlines():
			newline1 = line
			newline  = line
			if line[29:30] == "0" or line[29:30] == "1":
				newline = line[:29] + "1" + line[30:]
				newline1 = newline[:56] + "1.00" + newline[60:]
				newline = newline1[:108] + "     0" + newline1[114:]
				newline1 = newline[:132] + "     0" + newline[138:]
				newline = newline1[:156] + "     0" + newline1[162:]
				newline1 = newline[:180] + "     0" + newline[186:]
				newline = newline1[:204] + "     0" + newline1[210:]
				newline1 = newline
				#newline1 = newline[:228] + "     0" + newline[234:]
			output.append(newline1)

		pdb.close()
		
		try:
			outfile = open(pdbfile, 'w')
		except:
			print "unable to create output"
			sys.exit()

		for line in output:
			outfile.write(line)
		outfile.close()
		


if __name__ == "__main__":
	main()

