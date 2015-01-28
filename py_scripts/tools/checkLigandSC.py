#!/usr/bin/python

import string, sys, re, commands
from optparse import OptionParser
from file_routines import *
from Enzyme import *
from Selection import *


def main():

	"""
	checks the shape complementarity of the ligand in an enzyme
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		pdbfiles = files_from_list(options.pdblist)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()
	

	protein = Enzyme()
	sele = Selection()
	sele.makeSelection("element=C,N,O,S")
	tmp_pdbfile = "_tmpscpdb.pdb"

	input_file = "_sc_input"
	output_file = "_sc_output"
	try:
		SC_INPUT = open(input_file, 'w')
	except:
		print "unable to create temporary SC_INPUT"
		sys.exit()

	SC_INPUT.write("molecule 1\n")
	SC_INPUT.write("chain A\n")
	SC_INPUT.write("molecule 2\n")
	SC_INPUT.write("chain B\n")
	SC_INPUT.write("END\n")
	SC_INPUT.close()

	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		if protein.numChains() != 2:
			print pdbfile+": not enough chains",protein.numChains()
			protein.clear()
			continue

		protein.chain[0].name = "A"
		protein.chain[1].name = "B"
		newprot = sele.apply_selection(protein)
		newprot.writePDB(tmp_pdbfile)
		protein.clear()
		newprot.clear()

		commands.getoutput("sc XYZIN " + tmp_pdbfile + " SCRADII rosetta_radii.lib < " + input_file + " > " + output_file)
		ans = commands.getoutput("grep 'Shape complementarity statistic Sc' " + output_file)
		cols = ans.split()
		if len(cols) < 5:
			continue
		medSC = float(cols[5])
		ans = commands.getoutput("grep 'molecule 2 after trim' " + output_file)
		cols = ans.split()
		if len(cols) < 11:
			continue
		ndots1 = float(cols[10])
		print pdbfile,medSC,ndots1,medSC*ndots1
		commands.getoutput("rm -f " + output_file)
		commands.getoutput("rm -f " + tmp_pdbfile)

	commands.getoutput("rm -f " + input_file)




if __name__ == "__main__":
	main()
