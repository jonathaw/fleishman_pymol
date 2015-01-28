#!/usr/bin/python

import string, sys
from optparse import OptionParser


def main():

	"""

	transfers coordinates from a probe file onto a template file.  Only the 
	coordinate information is transfered over

	"""

	parser = OptionParser()
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-p", dest="probe", help="probe")
	parser.add_option("-P", dest="probelist", help="probelist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.target:
		parser.print_help()
		sys.exit()

	probes = []
	if options.probe:
		probes.append(options.probe)
	elif options.probelist:
		LIST = open(options.probelist)
		for line in LIST.readlines():
			line = string.rstrip(line)
			probes.append(line)
		LIST.close()
	else:
		parser.print_help()
		sys.exit()


	if options.outfile:
		if len(probes) > 1:
			print "cannot use -o option with -P"
			sys.exit()
		outfile = options.outfile
	elif options.replace:
		outfile = options.probe
	else:
		parser.print_help()
		sys.exit()

	TARGET = open(options.target)
	tarlines = TARGET.readlines()
	tarlines = filter(lambda x:x[0:6] in ("HETATM", "ATOM  "),tarlines)
	nlines = len(tarlines)
	TARGET.close()

	for prb in probes:
		PROBE  = open(prb)
		prblines = PROBE.readlines()
		PROBE.close()

		if options.replace:
			outfile = prb

		prblines = filter(lambda x:x[0:6] in ("HETATM", "ATOM  "),prblines)
		
		if len(prblines) != nlines:
			print "differing number of atom entries in target and probe"
			sys.exit()

		OUTPUT = open(outfile, 'w')	
		for i in range(nlines):
			tline = string.rstrip(tarlines[i])
			pline = string.rstrip(prblines[i])
			ml = len(tline)
			newline = tline[0:30] + pline[30:54] + tline[54:]
			OUTPUT.write(newline + "\n")

		OUTPUT.close()

if __name__ == "__main__":
	main()
