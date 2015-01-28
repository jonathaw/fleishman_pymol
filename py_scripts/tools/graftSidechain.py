#!/usr/bin/python


from Molecule import *
from ProteinLibrary import *
from optparse import OptionParser
import os, sys, string



def main():

	"""
	program to graft a sidechain from one protein, replacing another
	"""
	
	parser = OptionParser()
	parser.add_option("-t", dest="target",   help="target")
	parser.add_option("-p", dest="probe",   help="probe")
	parser.add_option("-o", dest="output",  help="output")
	parser.add_option("--ts", dest="target_side",  help="target sidechain")
	parser.add_option("--ps", dest="probe_side",  help="probe sidechain")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()


	if not options.target or not options.probe or not options.output:
		parser.print_help()
		sys.exit()

	if not options.target_side or not options.probe_side:
		parser.print_help()
		sys.exit()

	target = Molecule()
	target.readPDB(options.target)

	probe = Molecule()
	probe.readPDB(options.probe)

	probe_sc = probe.getResidue(options.probe_side)
	if probe_sc == None:
		print "unable to locate probe sidechain"
		sys.exit()

	print "grafting probe residue",probe_sc.name,probe_sc.file_id
	target.chain[0].replaceResidue(options.target_side, probe_sc)
	target.writePDB(options.output)
		


if __name__ == "__main__":
	main()
