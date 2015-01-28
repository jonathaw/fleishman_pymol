#!/usr/bin/python

import commands, os, sys, string, re, math
from file_routines import *


def get_surface_area(pdbfile, outbase):

	"""
	returns the surface area of the protein
	"""

	tmpfile = "_temp1_.pdb"
	sed = "sed '{s/ aroC /  C   /; s/CH1 / C  /; s/CH2 / C  /; s/CH3 / C  /; s/ CO.  /  C   /; s/HOH / O  /; s/ O..  /  O   /; s/ OCbb/  O  /; s/ Hpol /  H   /; s/ Hapo /  H   /; s/ Haro /  H   /; s/ N... /  N   /; s/ Phos /  P   /;  s/ Cl   /Cl  /; s/ Br   /  Br  /; s/ I    /  I   /; s/ F    /  F   /; s/ S    /  S   /;}' " + pdbfile + " > " + tmpfile
	os.system(sed)

	try:
		infile = open(tmpfile)
	except:
		print "surface_area: cannot open temporary file"
		return 0.0

	if "." in outbase:
		[base, rest] = outbase.split(".")
		outbase = base
	outpdb = outbase + ".pdb"

	try:
		outfile = open(outpdb, 'w')
	except:
		print "unable to open output pdb"
		sys.exit()

	for line in infile.readlines():
		words = string.split(line)
		if len(words) == 0: continue
		if words[0] != "ATOM" and words[0] != "HETATM": continue
		if len(words[2]) == 4 and words[2][0] == "V": continue
		if words[3] == "DOC": continue
		outfile.write(line[:54] + "\n")
	outfile.write("TER")
	outfile.close()

	home = os.environ['HOME']
	exe = home + "/code/naccess/naccess"
	if not exe_present(exe):
		exe = "/net/local/bin/naccess"
		if not exe_present(exe):
			print "cannot find naccess installed in:"
			print home + "/code/naccess/naccess"
			print "or"
			print exe
			sys.exit()

	cmd = exe + " " + outpdb + " -h"
	commands.getoutput(cmd)
	cmd = "rm -f " + tmpfile
	os.system(cmd)

	return 0.0

