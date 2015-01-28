#!/usr/bin/python

import os, sys, string
from Selection import *
from optparse import OptionParser

def main():

	"""
superimposes and reports the rmsd between two pdbfiles
(REQUIRES EXTERNAL BINARY: superimpose)
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="list", help="list")
	parser.add_option("-o", dest="outfile", help="output")
	parser.add_option("-s", dest="selection", help="selection")
	parser.add_option("-t", dest="target", help="target")
	parser.add_option("-p", dest="probe", help="probe")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	files = []
	if options.list:
		try:
			FILELIST = open(options.list, 'r')
		except:
			print "unable to open file list"
			sys.exit()

		for file in FILELIST.readlines():
			file = string.strip(file)
			files.append(file)
		FILELIST.close()	
	elif options.probe:
		files.append(options.probe)
	else:
		parser.print_help()
		sys.exit()

	if not options.target:
		parser.print_help()
		sys.exit()

	if options.outfile == None:
		parser.print_help()
		sys.exit()


	tmp_target = "_tmptarget.pdb"
	tmp_probe  = "_tmpprobe.pdb"
	if options.selection:
		makeSelection = "makeSelection.py -p " + options.target + " -o " + \
			tmp_target + " -s \"" + options.selection + "\""

		os.system(makeSelection)



	try:
		OUTFILE = open(options.outfile, 'w')
	except:
		print "unable to open outfile"
		sys.exit()


	

	for i in range(len(files)):
		firstName   = options.target
		currentName = files[i]
		firstFile   = options.target
		currFile    = files[i]

		if options.selection:
			currentFile = tmp_probe
			firstFile   = tmp_target

			makeSelection = "makeSelection.py -p " + files[i] + " -o " + \
				tmp_probe + " -s \"" + options.selection + "\""
			os.system(makeSelection)


		run = "rmsd " + firstFile + " " + currentFile
		sh = os.popen(run, 'r')
		line = sh.readline()
		rmsd = (string.split(line))[2]

		print "superimposing " + currentName + " to " + firstName + " => " + str(rmsd)
		OUTFILE.write(currentName + " " + firstName + " " + rmsd + "\n")

	OUTFILE.close()

	if options.selection:
		os.system("rm -f " + tmp_target)
		os.system("rm -f " + tmp_probe)


if __name__ == "__main__":
	main()
