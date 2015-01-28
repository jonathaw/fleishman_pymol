#!/usr/bin/python


import os, sys, string, commands
from optparse import OptionParser
from mol_routines import *
from Molecule import *
from Selection import *


def main():
	parser = OptionParser()
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-P", dest="probe", help="probe")
	parser.add_option("-s", dest="sele", help="sele")
	(options, args) = parser.parse_args()

	if not options.target or not options.probe:
		parser.print_help()
		sys.exit()

	try:
		PROBE = open(options.probe, 'r')
	except:
		print "unable to open probe list"
		sys.exit()

	prbMol = Molecule()
	trgMol = Molecule()

	[trg_start, trg_end] = options.sele.split("-")

	sel     = Selection()
	sel_str = "resi=" + trg_start + ";name= N  , CA , C  , O  "
	sel.makeSelection(sel_str)
	trgMol.readPDB(options.target)
	target = sel.apply_selection(trgMol)

	[base, rest] = options.target.split(".")
	newMol = 0
	for line in PROBE.readlines():
		line = string.rstrip(line)

		[file, start, end] = line.split()
		[id, rest] = file.split("_",1)
		[tmp, num] = rest.split("SLH_")
		outfile = base + "_" + id + "_" + num
		size = int(end) - int(start) + 1
		start = int(start)-1
		prb_start = start+1
		prb_end   = int(end)+1

		print file
		
		prbMol.readPDB(file)
		sel_str = "resi=" + str(start) + ";name= N  , CA , C  , O  "
		sel.clear()
		sel.makeSelection(sel_str)

		probe = sel.apply_selection(prbMol)

		superimpose_molecule(target, probe, prbMol)

		iprb1 = prbMol.chain[0].getResidueIndex(prb_start)
		iprb2 = prbMol.chain[0].getResidueIndex(prb_end)

		if iprb1 == None or iprb2 == None:
			print "cannot get index of ",prb_start

		iprb1 = int(iprb1)
		iprb2 = int(iprb2)
		prbslice = prbMol.chain[0].residue[iprb1:iprb2]
		newMol = trgMol.clone()

		beg = int(trg_start)
		end = int(trg_end)
		newMol.chain[0].slice(beg+1,end-1)
		newMol.chain[0].insertResidues(prbslice, beg)
		newMol.addRemark("REMARK LOOP INSERTION " + str(beg+1) + " " + str(beg+size))
		newMol.writePDB(outfile)

		probe.clear()
		prbMol.clear()
		newMol.clear()



if __name__ == "__main__":
	main()
