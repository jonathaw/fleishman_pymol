#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Enzyme import *
from Selection import *
from mol_routines import *
from file_routines import *


def main():

	"""
	finds the rms between two pdbfiles without superimposing
	"""

	parser = OptionParser()
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-p", dest="probe", help="probe")
	parser.add_option("-P", dest="probelist", help="probelist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-c", dest="centroid", help="center only", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()


	if not options.target:
		parser.print_help()
		sys.exit()

	probes = []
	if options.probelist:
		probes = files_from_list(options.probelist)
	elif options.probe:
		probes.append(options.probe)
	else:
		parser.print_help()
		sys.exit()

	target = Enzyme()
	probe  = Enzyme()

	target.readPDB(options.target)
	mysel = None
	if options.selection:
		mysel = Selection()
		mysel.makeSelection(options.selection)
		target = mysel.apply_selection(target)

	for probefile in probes:
		probe.readPDB(probefile)

		if options.selection:
			probe = mysel.apply_selection(probe)

		if options.centroid:
			tar_com = target.com()
			prb_com = probe.com()
			rms = tar_com.distance(prb_com)
		else:
			rms = fit(target,probe)
		print probefile,rms
		probe.clear()


if __name__ == "__main__":
	main()

