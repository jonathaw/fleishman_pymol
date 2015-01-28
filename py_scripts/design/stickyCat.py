#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Enzyme import *
from Selection import *

def main():

	"""
reads a rosetta output pdbfile and reports residues that have a total Eres  > cutoff
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-t", dest="type",    help="atom type", default="CS2 ")
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

	outfiles = []
	if options.outlist:
		outfiles = files_from_list(options.outlist)
	elif options.outfile:
		outfiles.append(options.outfile)
	elif options.replace:
		for file in pdbfiles:
			outfiles.append(file)
	else:
		parser.print_help()
		sys.exit()

	if len(pdbfiles) != len(outfiles):
		print "number of pdbfiles and output files differ"
		sys.exit()

	for i in range(len(pdbfiles)):
		pdbfile = pdbfiles[i]
		outfile = outfiles[i]

		commands.getoutput("cp " + pdbfile + " " + outfile)

		tmp = commands.getoutput("printCatRes.py -d -p " + pdbfile)
		cc  = tmp.split()
		cols = cc[1].split("_")

		for col in cols:
			nn = col.split("-")
			if nn[0] == "HIS":
				cmd = "addCentroid.py -w -t 'CS2 ' -p " + outfile + " -r -s 'resi=" + nn[1] + ";name= CG , ND1, CD2, CE1, NE2'"
				commands.getoutput(cmd)
			if nn[0] == "PHE":
				cmd = "addCentroid.py -w -t 'CS2 ' -p " + outfile + " -r -s 'resi=" + nn[1] + ";name= CG , CD1, CD2, CE1, CE2, CZ '"
				commands.getoutput(cmd)
			if nn[0] == "TYR":
				cmd = "addCentroid.py -w -t 'CS2 ' -p " + outfile + " -r -s 'resi=" + nn[1] + ";name= CG , CD1, CD2, CE1, CE2, CZ '"
				commands.getoutput(cmd)
			if nn[0] == "TRP":
				cmd = "addCentroid.py -w -t 'CS2 ' -p " + outfile + " -r -s 'resi=" + nn[1] + ";name= CD2, CE2'"
				commands.getoutput(cmd)
			if nn[0] == "SER":
				cmd = "addCentroid.py -w -t 'CS2 ' -p " + outfile + " -r -s 'resi=" + nn[1] + ";name= CB '"
				commands.getoutput(cmd)
			if nn[0] == "GLU":
				cmd = "addCentroid.py -w -t 'CS2 ' -p " + outfile + " -r -s 'resi=" + nn[1] + ";name= CG '"
				commands.getoutput(cmd)
			if nn[0] == "ASP":
				cmd = "addCentroid.py -w -t 'CS2 ' -p " + outfile + " -r -s 'resi=" + nn[1] + ";name= CB '"
				commands.getoutput(cmd)
			if nn[0] == "GLN":
				cmd = "addCentroid.py -w -t 'CS2 ' -p " + outfile + " -r -s 'resi=" + nn[1] + ";name= CG '"
				commands.getoutput(cmd)
			if nn[0] == "ASN":
				cmd = "addCentroid.py -w -t 'CS2 ' -p " + outfile + " -r -s 'resi=" + nn[1] + ";name= CB '"
				commands.getoutput(cmd)


if __name__ == "__main__":
	main()
