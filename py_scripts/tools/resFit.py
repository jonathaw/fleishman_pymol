#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from Selection import *
from mol_routines import *


def main():

	"""
	finds the residue-based rms between two pdbfiles without superimposing
	"""

	parser = OptionParser()
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-p", dest="probe", help="probe")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-c", dest="cutoff", help="cutoff")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()


	if not options.target or not options.probe:
		parser.print_help()
		sys.exit()

	target = Molecule()
	probe  = Molecule()

	target.readPDB(options.target)
	probe.readPDB(options.probe)

	if options.selection:
		mysel = Selection()
		mysel.makeSelection(options.selection)

		target = mysel.apply_selection(target)
		probe  = mysel.apply_selection(probe)

	rms = res_fit(target,probe)

	for line in rms:
		if options.cutoff:
			if float(line[1]) > float(options.cutoff):
				print line[0],line[1]
		else:
			print line[0],line[1]


if __name__ == "__main__":
	main()

