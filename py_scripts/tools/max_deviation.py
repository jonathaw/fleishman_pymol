#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from Selection import *
from mol_routines import *
from file_routines import *


def main():

	"""
reports the maximal distance between two sets of atoms
	"""

	parser = OptionParser()
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-p", dest="probe", help="probe")
	parser.add_option("-P", dest="probelist", help="probelist")
	parser.add_option("-s", dest="selection", help="selection")
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

	target = Molecule()
	probe  = Molecule()

	target.readPDB(options.target)
	mysel = None
	tlist = []
	if options.selection:
		mysel = Selection()
		mysel.makeSelection(options.selection)
		target = mysel.apply_selection(target)
	tlist = target.atomList()
	nlist = len(tlist)


	plist = []
	for probefile in probes:
		maxdist = 0.0
		probe.readPDB(probefile)

		if options.selection:
			probe = mysel.apply_selection(probe)

		plist = probe.atomList()

		if len(plist) != nlist:
			print "differing number of atoms"
			sys.exit()

		for i in range(nlist):
			dist = tlist[i].distance(plist[i])
			if dist > maxdist:
				maxdist = dist

		print probefile,maxdist
		probe.clear()


if __name__ == "__main__":
	main()

