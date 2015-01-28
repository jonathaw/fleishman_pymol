#!/usr/bin/python

from optparse import OptionParser
from Molecule import *
from Resfile import *
from file_routines import *
import string,sys


def main():

	"""
creates a resfile for domain assembly
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="regions", help="regions")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()


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
	else:
		parser.print_help()
		sys.exit()

	if (len(outfiles) != len(pdbfiles)):
		print "number of pdbfiles and outfiles differ"
		sys.exit()

	if not options.regions:
		parser.print_help()
		sys.exit()

	
	try:
		REGIONS = open(options.regions)
	except:
		print "unable to open regions file"
		sys.exit()

	
	# --- read regions file --- #
	beg = 0
	end = 0
	for line in REGIONS:
		line = string.rstrip(line)
		cols = line.split()
		beg  = int(cols[0])
		end  = int(cols[1])
		
	protein = Molecule()
	resfile = Resfile()
	cutoff  = 8.0

	for i in range(len(pdbfiles)):
		contacts = {}
		protein.readPDB(pdbfiles[i])
		resfile.setMolecule(protein)
		nres = protein.numResidues()

		chn = protein.chain[0]

		# --- set linker as repackable
		for j in range(beg,end+1):
			resfile.repackOnly(j)


		# --- get domain1 contacts
		for j in range(beg-1):
			datom1 = chn.residue[j].getAtom(" CB ")
			if datom1 == None:
				datom1 = chn.residue[j].getAtom(" CA ")
			for k in range(beg-1,nres):
				datom2 = chn.residue[k].getAtom(" CB ")
				if datom2 == None:
					datom2 = chn.residue[k].getAtom(" CA ")
				dist   = datom1.distance(datom2)

				if dist < cutoff:
					resfile.repackOnly(j)
					resfile.repackOnly(k)

		for j in range(beg-1,end):
			datom1 = chn.residue[j].getAtom(" CB ")
			if datom1 == None:
				datom1 = chn.residue[j].getAtom(" CA ")
			for k in range(end+1,nres):
				datom2 = chn.residue[k].getAtom(" CB ")
				if datom2 == None:
					datom2 = chn.residue[k].getAtom(" CA ")
				dist   = datom1.distance(datom2)

				if dist < cutoff:
					resfile.repackOnly(j)
					resfile.repackOnly(k)

		resfile.write(outfiles[i])	
		protein.clear()


if __name__ == "__main__":
	main()
