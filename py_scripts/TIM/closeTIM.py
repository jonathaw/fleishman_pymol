#!/usr/bin/python

"""

	closeTIM.py

	closes the break points in a TIM barrel protein

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import os, sys, string, commands
from optparse import OptionParser
from mol_routines import *
from Molecule import *
from Selection import *


def main():
	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-n", dest="name", help="name")
	parser.add_option("-c", dest="chain", help="chain")
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		try:
			PDBLIST = open(options.pdblist, 'r')
		except:
			print "unable to open pdblist"
			sys.exit()

		for line in PDBLIST.readlines():
			line = string.rstrip(line)
			pdbfiles.append(line)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()


	if not options.name:
		parser.print_help()
		sys.exit()


	if not options.chain:
		parser.print_help()
		sys.exit()

	protein = Molecule()
	for pdbfile in pdbfiles:
		ans = ""
		ans = commands.getoutput("grep INSERT " + pdbfile)
		cols = ans.split()
		beg = cols[3]
		end = cols[4]
		newfile = options.name + options.chain + ".pdb"
		rosexe  = "loop.gcc lp " + options.name + " " + options.chain + " -s " + pdbfile
		rosexe += " -pose_looping -loop_begin " + beg + " -loop_end " + end
		rosexe += " -loop_cutpoint " + end + " -ccd_closure -nstruct 1"

		# ===   get fasta file
		os.system("cp " + pdbfile + " " + newfile)
		os.system("makeFasta.pl -p " + newfile)
		os.system(rosexe)

		out = "lp" + options.name + "0001.pdb"
		[base,rest] = pdbfile.split(".")
		newout = base + "_close.pdb"
		os.system("mv " + out + " " + newout)
		os.system("rm lp" + options.name + ".fasc")

		protein.readPDB(newout)
		protein.addRemark(ans)
		protein.writePDB(newout)
		protein.clear()




if __name__ == "__main__":
	main()
