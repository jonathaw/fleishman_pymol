#!/usr/bin/python


import os, sys, string
from optparse import OptionParser
from TIM import *
from SecondaryStructure import *


def main():
	parser = OptionParser()
	parser.add_option("-s", dest="ssfile",  help="ssfile")
	parser.add_option("-t", dest="timfile", help="timfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-c", dest="color",   help="color")
	parser.add_option("-x", dest="extract", help="extract", action="store_true")
	(options, args) = parser.parse_args()


	timmeh = TIM()
	secstruc = SecondaryStructure()
	if options.ssfile:
		secstruc.readSSfile(options.ssfile)
		timmeh.setSequence(secstruc.sequence)
	elif options.timfile:
		timmeh.readTIM(options.timfile)
	else:
		parser.print_help()
		sys.exit()

	if options.outfile:
		timmeh.writeTIM(options.outfile)

	if options.color:
		timmeh.writePymol(options.color)


			

if __name__ == "__main__":
	main()
