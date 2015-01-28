#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from Molecule import *
from Selection import *
import os, sys, string
from optparse import OptionParser

def main():
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-t", dest="TIMfile", help="TIMfile")
	(options, args) = parser.parse_args()

	if not options.pdbfile or not options.TIMfile:
		parser.print_help()
		sys.exit()

	# ===   read the TIMfile   === #
	try:
		TIMFILE = open(options.TIMfile, 'r')
	except:
		print "unable to open TIMfile"


	(basename,other) = options.pdbfile.split(".",2)
	print "basename = ",basename
	
	Sel = Selection()	
	protein = Molecule()
	protein.readPDB(options.pdbfile)

	cols = []
	stripped = 0
	nHLS = 0
	nSLH = 0
	for line in TIMFILE.readlines():	
		line = string.strip(line)
		cols = line.split()
		if len(cols) == 0:
			if stripped:
				stripped.writePDB(outname)

			continue

		if cols[0] == "SLH":
			nSLH += 1
			startX = cols[2]
			endX   = cols[3]

			Sel.clear()
			Sel.makeSelection("resi=" + str(startX) + "-" + str(endX))
			stripped = Sel.apply_selection(protein)
			outname  = basename + "_SLH_" + str(nSLH) + ".pdb"

		if cols[0] == "HLS":
			nHLS += 1
			startX = cols[2]
			endX   = cols[3]

			Sel.clear()
			Sel.makeSelection("resi=" + str(startX) + "-" + str(endX))
			stripped = Sel.apply_selection(protein)
			outname  = basename + "_HLS_" + str(nHLS) + ".pdb"

		if cols[0] == "HELIX":
			startH = cols[2]
			endH   = cols[3]
			myStart = int(startH) - int(startE) + 1
			myEnd   = int(endH) - int(startE) + 1
			mySize  = myEnd - myStart +1
			stripped.addRemark("REMARK HELIX " + str(mySize) + " " + str(myStart) + " " + str(myEnd))

		if cols[0] == "LOOP":
			startL = cols[2]
			endL   = cols[3]
			myStart = int(startL) - int(startE) + 1
			myEnd   = int(endL) - int(startE) + 1
			mySize  = myEnd - myStart +1
			#stripped.addRemark("REM LOOP  " + startL + " " + endL)
			stripped.addRemark("REMARK LOOP  " + str(mySize) + " " + str(myStart) + " " + str(myEnd))

		if cols[0] == "SHEET":
			startE = cols[2]
			endE   = cols[3]
			myEnd = int(endE) - int(startE) + 1
			mySize = myEnd
			#stripped.addRemark("REM SHEET " + startE + " " + endE)
			stripped.addRemark("REMARK SHEET " + str(mySize) + " 1 " + str(myEnd))

	TIMFILE.close()

		 		

if __name__ == "__main__":
	main()
	

