#!/usr/bin/python

from optparse import OptionParser
import os, sys, string, re, commands
from file_routines import *

def main():

	"""
copies REMARK information from one pdbfile to another
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-i", dest="header", help="header")
	parser.add_option("-o", dest="outfile",  help="outfile")
	parser.add_option("-O", dest="outlist",  help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-e", dest="extension", help="file extension (eg _packing)")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	# setup files
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

	if len(outfiles) != len(pdbfiles):
		print "number of files differ"
		sys.exit()

	for i in range(len(pdbfiles)):
		header = ""
		if not options.header:
			if options.extension:
				header = pdbfiles[i].replace(options.extension, "")
			else:
				parser.print_help()
				sys.exit()
		else:
			header = options.header
	
			
		commands.getoutput("grep REMARK " + header + " > _head")
		commands.getoutput("cat _head " + pdbfiles[i] + " > _inter")
		commands.getoutput("mv _inter " + outfiles[i])
		commands.getoutput("rm -f _head")


if __name__ == "__main__":
	main()
