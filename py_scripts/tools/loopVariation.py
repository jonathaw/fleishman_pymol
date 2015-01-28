#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from Selection import *
from mol_routines import *


def main():

	"""
	measures the rmsd variation in a loop
	"""

	parser = OptionParser()
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-l", dest="loop", help="loop")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()


	pdbfiles = []
	if options.pdblist:
		try:
			LIST = open(options.pdblist)
		except:
			print "unable to open pdblist:",options.pdblist
			sys.exit()

		for line in LIST.readlines():
			line = string.rstrip(line)
			pdbfiles.append(line)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	if not options.target:
		parser.print_help()
		sys.exit()

	if not options.loop:	
		parser.print_help()
		sys.exit()

	(bl, el) = options.loop.split("-")
	beg_loop = int(bl) - 1
	end_loop = int(el) + 1
	loopsel = ";resi=1-" + str(beg_loop) + "," + str(end_loop) + "-5000"

	target = Molecule()
	target.readPDB(options.target)

	selBB   = "name= N  , CA , C  , O  "
	selLoop = selBB + loopsel

	myselBB   = Selection()
	myselLoop = Selection()

	myselBB.makeSelection(selBB)
	myselLoop.makeSelection(selLoop)

	tarBB   = myselBB.apply_selection(target)
	tarloop = myselLoop.apply_selection(target)

	
	probe = Molecule()
	for pdb in pdbfiles:
		probe.readPDB(pdb)
		probeloop = myselLoop.apply_selection(probe)
		probeBB   = myselBB.apply_selection(probe)

		superimpose_molecule(tarloop,probeloop,probeBB)
		print "tarBB = ",tarBB.numAtoms()
		print "probeBB = ",probeBB.numAtoms()
		rms = fit(tarBB,probeBB)
		print "rms = ",rms

		probeloop.clear()
		probeBB.clear()
		probe.clear()



if __name__ == "__main__":
	main()

