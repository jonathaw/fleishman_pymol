#!/usr/bin/python

import commands, os, sys, string, re, math



def files_from_list(file):
	
	"""
	returns a list of files from a file
	"""

	files = []
	try:
		MYFILE = open(file)
	except:
		print "unable to open file:",file
		return files

	for line in MYFILE:
		line = line.rstrip()
		files.append(line)

	MYFILE.close()

	return files



def get_basefile(file=""):

	"""
	returns the basefile assuming a '.' as the delimiter
	"""

	base = ""
	if file == "":
		return base

	#[base, suffix] = file.rsplit(".",1)
	#[base, suffix] = string.rsplit(file, ".")
	dot_index = file.rindex(".")
	base = file[0:dot_index]
	return base



def exe_present(exe=""):

	"""
	checks to see if an executable is present
	"""

	if exe == "":
		return False

	answer = commands.getoutput("which " + exe)
	answer = string.rstrip(answer)

	exe_present = re.compile("no " + exe + " in")

	if exe_present.search(answer):
		return False

	return True
