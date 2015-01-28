#!/usr/bin/python

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"


import os, sys, string,re
import commands
from file_routines import *


def run_dssp(pdbfile):

	"""
runs the dssp executable to determine the secondary structural
content of a protein.  Returns a string
	"""

	dssp_exe = "dssp"

	answer = commands.getoutput("which " + dssp_exe)
	answer = string.rstrip(answer)

	exe_present = re.compile("no " + dssp_exe + " in")

	if exe_present.match(answer):
		print "WARNING: dssp executable not present"
		return -1

	tmpfile  = "_tmpfile_"

	commands.getoutput(dssp_exe + " " + pdbfile + " " + tmpfile)	

	try:
		DSSP = open(tmpfile, 'r')
	except:
		print "unable to open dssp file"
		return

	bRead = 0
	ss = ""
	for line in DSSP.readlines():
		line = string.rstrip(line)
		if line[0:3] == "  #":
			bRead = 1
			continue

		if bRead:
			ts = line[16:17]
			if ts != "H" and ts != "E":
				ts = "L"

			ss += ts

	DSSP.close()
	return ss



def run_stride(pdbfile):

	"""
runs the stride secondary structure determination program.  Returns a string
	"""

	stride_exe = "stride"

	answer = commands.getoutput("which " + stride_exe)
	answer = string.rstrip(answer)

	exe_present = re.compile("no " + stride_exe + " in")

	if exe_present.match(answer):
		print "WARNING: stride executable not present"
		return -1

	tmpfile  = "_tmpfile_"

	commands.getoutput(stride_exe + " -o " + pdbfile + " -f" + tmpfile)	

	try:
		STRIDE = open(tmpfile, 'r')
	except:
		print "unable to open stride file"
		return

	sec = re.compile("^STR")
	seq = re.compile("^SEQ")

	maxres = 0
	ssline = ""
	for line in STRIDE.readlines():
		line = string.rstrip(line)

		if seq.match(line):
			maxres = int(line[62:66])
			
		
		if sec.match(line):
			ssline += line[10:60]

	ss = ""
	for i in range(maxres):
		if ssline[i] != "H" and ssline[i] != "E":
			ss += "L"
		else:
			ss += ssline[i]
			
	return ss



def getSecondaryStructure(file=""):

	"""
	returns the secondary structure
	first tries dssp 
	else tries stride
	"""

	if exe_present("dssp"):
		return run_dssp(file)
	elif exe_present("stride"):
		return run_stride(file)
	else:
		print "secondary structure executable not found"
		return ""
