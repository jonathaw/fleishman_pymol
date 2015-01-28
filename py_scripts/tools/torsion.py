#!/usr/bin/python

from Torsions import *
from Molecule import *
from optparse import OptionParser
import sys, os, string



def main():

	"""
reports the torsional angles in a pdbfile
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="selection", help="selection")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	
	pdbfiles = []
	if options.pdblist:
		try:
			PDBLIST = open(options.pdblist)
		except:
			print "unable to open pdblist",options.pdblist
			sys.exit()

		for line in PDBLIST.readlines():
			pdbfiles.append(line)

	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()
	

	if options.selection:
		selection = Selection()
		selection.makeSelection(options.selection)

	protein = Molecule()
	torsion = Torsions()
	torsion.readTorsions()


	for pdbfile in pdbfiles:
		protein.clear()
		protein.readPDB(pdbfile)

		for chain in protein.chain:
			for residue in chain.residue:
				phi  = torsion.getTorsion(chain, residue.file_id, "PHI")
				psi  = torsion.getTorsion(chain, residue.file_id, "PSI")
				ome  = torsion.getTorsion(chain, residue.file_id, "OME")
				chi1 = torsion.getTorsion(chain, residue.file_id, "CHI1")
				chi2 = torsion.getTorsion(chain, residue.file_id, "CHI2")
				chi3 = torsion.getTorsion(chain, residue.file_id, "CHI3")
				chi4 = torsion.getTorsion(chain, residue.file_id, "CHI4")

				out = pdbfile + ":  " + residue.file_id + "  " + residue.name + \
					"  %8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f" % (phi,psi,ome,chi1,chi2,chi3,chi4)

				print out



if __name__ == "__main__":
	main()


