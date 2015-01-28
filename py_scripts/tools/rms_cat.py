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
	parser.add_option("-c", dest="catalytic", help="catalytic residue")
	parser.add_option("-H", dest="heavy", help="heavy atom only", action="store_true")
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

	if not options.catalytic:
		parser.print_help()
		sys.exit()

	target = Enzyme()
	probe  = Enzyme()

	target.readPDB(options.target)

	icat = int(options.catalytic)-1
	if icat > len(target.catalytic):
		print "accessing catalytic residue out of bounds"
		sys.exit()

	tar_cat = target.catalytic[icat]
	tlist = []
	if options.heavy:
		for atm in tar_cat.atom:
			if atm.element != "H":
				tlist.append(atm)
	else:
		tlist = tar_cat.atom

	for probefile in probes:
		probe.readPDB(probefile)

		if icat > len(probe.catalytic):
			print "accessing catalytic residue out of bounds"
			sys.exit()

		prb_cat = probe.catalytic[icat]
		plist = []
		if options.heavy:
			for atm in prb_cat.atom:
				if atm.element != "H":
					plist.append(atm)
		else:
			plist = prb_cat.atom

		rms = fitAtomList(tlist,plist)
		print probefile,rms
		probe.clear()


if __name__ == "__main__":
	main()

