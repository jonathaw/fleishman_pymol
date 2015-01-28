#!/usr/bin/python

import os, sys, string
from optparse import OptionParser



def main():

	"""
performs a set of instructions in multiple directories in the present working directory
	"""

	parser = OptionParser()
	parser.add_option("-i", dest="input", help="input")
	parser.add_option("-e", dest="execute", help="execute")
	parser.add_option("-d", dest="directory", help="directory")
	parser.add_option("-D", dest="dirlist", help="dirlist")
	parser.add_option("-p", dest="pwd", help="print working directory",action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	input = []
	if options.input:
		try:
			INPUT = open(options.input)
		except:
			print "unable to open input"
			sys.exit()

		for line in INPUT.readlines():
			line = string.strip(line)
			input.append(line)

	elif options.execute:
		input.append(options.execute)
	else:
		parser.print_help()
		sys.exit()

	
	dirlist = []
	if options.dirlist:
		try:
			DIRLIST = open(options.dirlist)
		except:
			print "unable to open dirlist"
			sys.exit()

		for line in DIRLIST.readlines():
			line = string.strip(line)
			dirlist.append(line)
	
	elif options.directory:
		dirlist.append(options.directory)
	else:
		pwd = os.getcwd()
		tmplist = os.listdir(pwd)
		for dir in tmplist:
			if os.path.isdir(dir):
				dirlist.append(dir)

	
	for dir in dirlist:
		if options.pwd:
			print dir
		os.chdir(dir)
		for exe in input:
			os.system(exe)

		os.chdir("..")
	




if __name__ == "__main__":
	main()
