#!/usr/bin/python

import string, sys, os, commands, re, stat
from optparse import OptionParser
from file_routines import *

def main():

	"""
	Goes through and scans all ligands for matches in a directory
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="liglist", help="list of ligands")
	parser.add_option("-r", dest="runfile", help="run file")
	parser.add_option("-o", dest="logfile", help="log file")
	parser.add_option("-b", dest="bkupfile", help="backed up file")
	parser.add_option("-g", dest="go", help="do the runs",action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.liglist or not options.runfile:
		parser.print_help()
		sys.exit()

	if not options.logfile:
		parser.print_help()
		sys.exit()

	# --- create directories for each ligand --- #	
	ligands = files_from_list(options.liglist)	

	exe = "basename $PWD"
	currdir = commands.getoutput(exe)

	cwd = os.getcwd()
	ls = os.listdir(cwd)
	protein = currdir + "_9.pdb"
	if not protein in ls:
		print "cannot find protein file:",protein
		sys.exit()

	try:
		RUN = open(options.runfile)
	except:
		print "unable to open run file"
		sys.exit()	

	runline = RUN.readline()
	re_het  = re.compile("HETERO")
	re_prt  = re.compile("PROTEIN")

	if not re_het.search(runline):
		print "run must contain HETERO"
		sys.exit()

	if not re_prt.search(runline):
		print "run must contain PROTEIN"
		sys.exit()
		

	for lig in ligands:
		rline = runline
		ligbase = get_basefile(lig)

		exe = "mkdir " + ligbase
		os.system(exe)

		exe = "cp " + lig + " " + ligbase
		os.system(exe)

		exe = "cp " + currdir + "* " + ligbase
		os.system(exe)

		exe = "cp paths.txt " + ligbase
		os.system(exe)

		exe = "cp " + options.bkupfile + " " + ligbase
		os.system(exe)

		rline = rline.replace("HETERO", lig)
		rline = rline.replace("PROTEIN", protein)
		
		newrun = ligbase + "/" + options.runfile
		try:
			OUTRUN = open(newrun, 'w')
		except:
			print "cannot make new run"
			sys.exit()


		OUTRUN.write(rline) 
		OUTRUN.close()
		os.chmod(newrun, stat.S_IRWXU)

		if options.go:
			os.chdir(ligbase)
			print "   in",os.getcwd()
			exe = "nice ./" + options.runfile + " >& " + options.logfile
			os.system(exe)
			os.chdir("..")	


if __name__ == "__main__":
	main()

