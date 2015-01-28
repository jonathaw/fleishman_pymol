#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string, sys, os, commands
from optparse import OptionParser


def main():

	"""
fixes a problem where backedup residues are incorrectly numbered in the header section
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="list", help="list of files")
	parser.set_description(main.__doc__)


	(options, args) = parser.parse_args()

	if options.list == None:
		parser.print_help()
	
	try:
		PDBLIST = open(options.list)
	except:
		print "unable to open list"
		sys.exit()

	files = []
	for file in PDBLIST.readlines():
		file = string.strip(file)
		files.append(file)

	if len(files) == 0:
		sys.exit()
		
	for file in files:
		ans = commands.getoutput("grep 'REMARK BACKBONE TEMPLATE A LG1' " + file)	
		tmp = ans.split("\n")
		for line in tmp:
			cols = line.split()
			if int(cols[11]) == 1:
				tmpvar = line[54:59]

		ans = commands.getoutput("grep 'REMARK BACKBONE TEMPLATE A HIS' " + file)
		cols = ans.split()
		newvar = "REMARK BACKBONE TEMPLATE A HIS" + tmpvar
		#print ans[0:35]+"*"
		commands.getoutput("rpl '"+ans[0:35]+"' '"+newvar+"' " + file)

				


if __name__ == "__main__":
	main()
