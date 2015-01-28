#!/usr/bin/python

import os, sys, string
from Selection import *
from optparse import OptionParser
from mol_routines import *
from file_routines import *

def main():

	"""
Superimposes a probe molecule onto a target molecule.
Selections for the target and probe may be given.
If a probe selection is given but not an explicit target selection
that selection is applied to BOTH molecules
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="list", help="probe list")
	parser.add_option("-o", dest="outfile", help="output")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-S", dest="target_selection", help="target selection")
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-p", dest="probe", help="probe")
	parser.add_option("-v", dest="verbose", help="verbose", action="store_true")
	parser.add_option("-r", dest="remark", help="add remark to pdb", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	files = []
	if options.list:
		files = files_from_list(options.list)
	elif options.probe:
		files.append(options.probe)
	else:
		parser.print_help()
		sys.exit()

	if not options.target:
		parser.print_help()
		sys.exit()

	outfiles = []
	if options.outlist:
		outfiles = files_from_list(options.outlist)
	elif options.outfile:
		outfiles.append(options.outfile)
	else:
		parser.print_help()
		sys.exit()


	target = Molecule()	
	target.readPDB(options.target)
	sele = Selection()
	if options.target_selection:
		sele.makeSelection(options.target_selection)
		target = sele.apply_selection(target)
	elif options.selection:
		sele.makeSelection(options.selection)
		target = sele.apply_selection(target)

	sele.clear()
	if options.selection:
		sele.makeSelection(options.selection)
	
	probe = Molecule()
	myrmsd = 0.0
	for i in range(len(files)):
		probe.readPDB(files[i])

		new_probe = probe
		if options.selection:
			new_probe = sele.apply_selection(probe)

		myrmsd = superimpose_molecule(target, new_probe, probe)

		if options.verbose:
			print files[i],"rmsd=",myrmsd

		if options.remark:
			probe.addRemark("REMARK RMSD = " + str(myrmsd))

		probe.writePDB(outfiles[i],resRenumber=False,atomRenumber=False)
		probe.clear()



if __name__ == "__main__":
	main()
