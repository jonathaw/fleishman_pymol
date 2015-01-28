#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import os, sys, string, commands
from optparse import OptionParser



def main():

	"""
creates multiple posfiles based on a 'report_match_only' flag from a matching log file
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="log", help="log")
	parser.add_option("-b", dest="base", help="base file name")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	if not options.log or not options.base:
		parser.print_help()
		sys.exit()

	pos0 = options.base + ".pos0"	
	pos1 = options.base + ".pos1"
	pos2 = options.base + ".pos2"
	pos3 = options.base + ".pos3"
	pos4 = options.base + ".pos4"


	cmd0 = "grep 'match f' " + options.log + " | sort -n +2 | uniq | grep ': 1' | awk '{print $5}' | sort -n | uniq"
	cmd1 = "grep 'match f' " + options.log + " | sort -n +2 | uniq | grep ': 2' | awk '{print $5}' | sort -n | uniq"
	cmd2 = "grep 'match f' " + options.log + " | sort -n +2 | uniq | grep ': 3' | awk '{print $5}' | sort -n | uniq"
	cmd3 = "grep 'match f' " + options.log + " | sort -n +2 | uniq | grep ': 4' | awk '{print $5}' | sort -n | uniq"
	cmd4 = "grep 'match f' " + options.log + " | sort -n +2 | uniq | grep ': 5' | awk '{print $5}' | sort -n | uniq"

	ans0 = commands.getoutput(cmd0)
	ans1 = commands.getoutput(cmd1)
	ans2 = commands.getoutput(cmd2)
	ans3 = commands.getoutput(cmd3)
	ans4 = commands.getoutput(cmd4)

	c0 = ans0.split()
	if len(c0) > 0:
		FILE0 = open(pos0, 'w')
		for x in c0:
			FILE0.write(x + " ")
		FILE0.write("\n")
		FILE0.close()

	c1 = ans1.split()
	if len(c1) > 0:
		FILE1 = open(pos1, 'w')
		for x in c1:
			FILE1.write(x + " ")
		FILE1.write("\n")
		FILE1.close()

	c2 = ans2.split()
	if len(c2) > 0:
		FILE2 = open(pos2, 'w')
		for x in c2:
			FILE2.write(x + " ")
		FILE2.write("\n")
		FILE2.close()

	c3 = ans3.split()
	if len(c3) > 0:
		FILE3 = open(pos3, 'w')
		for x in c3:
			FILE3.write(x + " ")
		FILE3.write("\n")
		FILE3.close()

	c4 = ans4.split()
	if len(c4) > 0:
		FILE4 = open(pos4, 'w')
		for x in c4:
			FILE4.write(x + " ")
		FILE4.write("\n")
		FILE4.close()

if __name__ == "__main__":
	main()
