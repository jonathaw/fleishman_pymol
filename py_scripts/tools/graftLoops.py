#!/usr/bin/python


from Molecule import *
from ProteinLibrary import *
from optparse import OptionParser
import os, sys, string, re
from mol_routines import *
from match_routines import *
from file_routines import *



def main():

	"""
	grafts loops from a loop library onto a ligand dumpfile
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="scaffold", help="scaffold")
	parser.add_option("-o", dest="outfile",  help="outfile")
	parser.add_option("-O", dest="outlist",  help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-l", dest="loop_lib", help="loop_library")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()

	outfiles = []
	if options.outlist:
		outfiles = files_from_list(options.outlist)
	elif options.outfile:
		outfiles.append(options.outfile)
	elif options.replace:
		outfiles = pdbfiles
	else:
		parser.print_help()
		sys.exit()

	if not options.scaffold:
		parser.print_help()
		sys.exit()

	if not options.loop_lib:
		parser.print_help()
		sys.exit()


	protein = Molecule()
	protein.readPDB(options.scaffold)
	scaffold = protein.getChain("A")

	# read in loop library
	try:
		LOOP_LIB = open(options.loop_lib)
	except:
		print "unable to open loop library"
		sys.exit()

	cols = []
	for line in LOOP_LIB.readlines():
		line = string.rstrip(line)
		cols = line.split()
		print cols[0]

	sys.exit()
	mol = Molecule()
	for i in range(len(pdbfiles)):
		print pdbfiles[i]
		chainA = scaffold.clone()
	
		mol.readPDB(pdbfiles[i])	
		chainB = mol.getChain("B")
		chainB.renumber(atomRenumber=False)

		mol.chain.insert(0,chainA)
		mol.writePDB(outfiles[i], resRenumber=False, atomRenumber=False)
		mol.clear()

		


if __name__ == "__main__":
	main()
