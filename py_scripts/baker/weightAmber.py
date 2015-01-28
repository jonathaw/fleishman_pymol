#!/usr/bin/python

import string, sys
from optparse import OptionParser


def main():

	"""
applies weights to a given amber score file
	"""

	parser = OptionParser()
	parser.add_option("-i", dest="input", help="input")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.input or not options.outfile:
		parser.print_help()
		sys.exit()

	try:
		INP = open(options.input)
	except:
		print "unable to open input"
		sys.exit()

	try:
		OUT = open(options.outfile, 'w')
	except:
		print "unable to open outfile"
		sys.exit()

	for line in INP.readlines():
		line = string.rstrip(line)
		if line[0:4] == "FILE":
			continue

		cols = line.split()
		Evdw = float(cols[4]) + float(cols[5])
		Eele = float(cols[6]) + float(cols[7])
		Esol = float(cols[8]) + float(cols[9])

		Etot = 0.378*Evdw + 0.310*Eele + 0.312*Esol
		OUT.write(cols[0] + "   " + str(Etot) + "\n")
	OUT.close()
	INP.close()





if __name__ == "__main__":
	main()
