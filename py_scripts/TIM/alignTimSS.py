#!/usr/bin/python

"""

	alignTimSS

	aligns TIM barrel proteins based on their secondary structure

"""


import os, sys, string
from optparse import OptionParser
from TIM import *
from SecondaryStructure import *

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


def main():

	"""
	"""

	parser = OptionParser()
	parser.add_option("-s", dest="ssfile",  help="ssfile")
	parser.add_option("-t", dest="timfile", help="timfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	(options, args) = parser.parse_args()


	timmeh = TIM()
	sec = SecondaryStructure()
	if options.ssfile:
		sec.readSSfile(options.ssfile)
		sec.sequence = seq
	else:
		parser.print_help()
		sys.exit()

	if options.timfile:
		timmeh.readTIM(options.timfile)



	SSstring  = sec.formatSequence()
	TIMstring = timmeh.formatSegments()

	ssarray = SSstring.split("\n")
	timarray = TIMstring.split("\n")

	ns = len(ssarray)	
	ts = len(timarray)

	for i in range(ts):
		sl = len(timarray[i])
		match = ""
		for j in range(sl):
			if timarray[i][j] == " ":
				match += " "
				continue

			if timarray[i][j] == ssarray[i][j]:
				match += "|"

		print ssarray[i]
		print match
		print timarray[i]
		print ""

			

if __name__ == "__main__":
	main()
