#!/usr/bin/python

import string, sys, re
from optparse import OptionParser
from file_routines import *

def main():

	"""
reports a list of unique matches.  This is defined by the identity of the 
catalytic residues and the position of space of the ligand (discreteness defined
by the "fineness" option)
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="file_list", help="file list")
	parser.add_option("-u", dest="unique", help="unique list")
	parser.add_option("-c", dest="constraint", help="constraint")
	parser.add_option("-r", dest="repulsive", help="repulsive")
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file_list or not options.unique or not options.constraint or not options.repulsive:
		parser.print_help()
		sys.exit()

	try:
		LIST = open(options.file_list)
	except:
		print "unable to open file list:",options.file_list
		sys.exit()

	try:
		UNIQUE = open(options.unique)
	except:
		print "unable to open unique:",options.unique
		sys.exit()

	try:
		CONSTRAINT = open(options.constraint)
	except:
		print "unable to open constraints:",options.constraint
		sys.exit()

	try:
		REPULSIVE = open(options.repulsive)
	except:
		print "unable to open repulsive:",options.repulsive
		sys.exit()

	file_list = []
	for line in LIST.readlines():
		file_list.append(string.rstrip(line))

	nline = len(file_list)

	uniq_list = []
	for line in UNIQUE.readlines():
		uniq_list.append(string.rstrip(line))

	if nline != len(uniq_list):
		print "uniq - wrong number of lines"
		sys.exit()
		
	cnst_list = []
	for line in CONSTRAINT.readlines():
		cnst_list.append(string.rstrip(line))

	if nline != len(cnst_list):
		print "cnst - wrong number of lines"
		sys.exit()
		
	repl_list = []
	for line in REPULSIVE.readlines():
		repl_list.append(string.rstrip(line))

	if nline != len(repl_list):
		print "repl - wrong number of lines"
		sys.exit()

	uniq_key = {}
	for line in uniq_list:
		cols = line.split()

		if not cols[1] in uniq_key.keys():
			uniq_key[cols[1]] = []

		uniq_key[cols[1]].append(cols[0])


	cnst_key = {}
	for line in cnst_list:
		cols = line.split()
		cnst_key[cols[0]] = cols[1]

	repl_key = {}
	for line in repl_list:
		cols = line.split()
		repl_key[cols[0]] = cols[1]

	keeplist = []
	for key in uniq_key.keys():
		# pick best cst energy	
		bestE = 99999.0
		for e in cnst_key.keys():
			if e in uniq_key[key]:
				if float(cnst_key[e]) < bestE:
					bestE = float(cnst_key[e])

		tmplist = {}
		for e in cnst_key.keys():
			if e in uniq_key[key]:
				if float(cnst_key[e]) == bestE:
					tmplist[e] = 1

		# pick best repulsive energy
		bestE = 99999.0
		bestF = 0
		for e in tmplist.keys():
			if float(repl_key[e]) < bestE:
				bestF = e
				bestE = float(repl_key[e])
				
		keeplist.append(bestF)

	if not options.inverse:
		for file in keeplist:
			print file
	else:
		for file in file_list:
			if not (file in keeplist):
				print file
			
		

	LIST.close()
	UNIQUE.readlines()
	CONSTRAINT.readlines()
	REPULSIVE.readlines()



if __name__ == "__main__":
	main()
