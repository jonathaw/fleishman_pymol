#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Selection import *
from Molecule import *


def main():

	"""

	swaps residues from one pdbfile into another
	the number of residues may differ

	"""

	parser = OptionParser()
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-p", dest="probe", help="probe")
	parser.add_option("-P", dest="probelist", help="probelist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("--ts", dest="target_selection", help="target selection eg (51-63)")
	parser.add_option("--ps", dest="probe_selection", help= "probe selection eg (51-63)")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.target:
		parser.print_help()
		sys.exit()

	probes = []
	if options.probe:
		probes.append(options.probe)
	elif options.probelist:
		probes = files_from_list(options.probelist)
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


	if not options.target_selection or not options.probe_selection:
		parser.print_help()
		sys.exit()

	target = Molecule()
	probe  = Molecule()

	target.readPDB(options.target)
	probe.readPDB(options.probe)

	tmp = options.target_selection.split("-")
	tar_beg = int(tmp[0])
	tar_end = int(tmp[1])

	tmp = options.probe_selection.split("-")
	prb_beg = int(tmp[0])
	prb_end = int(tmp[1])

	target.chain[0].slice(tar_beg,tar_end)
	prblist = probe.chain[0].getResidues(prb_beg, prb_end)
	target.chain[0].insertResidues(prblist, tar_beg-1)

	target.writePDB(outfile)




if __name__ == "__main__":
	main()
