#!/usr/bin/python

from optparse import OptionParser
import sys, string
from Enzyme import *
from Selection import *
from match_routines import *
from mol_routines import *
from file_routines import *


def main():

	"""
points hydrogens on H-bond donors (SER and TYR) towards an H-bond acceptor)
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
#	parser.add_option("-o", dest="outfile", help="outfile")
#	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-d", dest="donor", help="donor residue")
	parser.add_option("-c", dest="catalytic", help="catalytic residue")
	parser.add_option("-a", dest="acceptor", help="acceptor atom")
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

	if not options.acceptor:
		parser.print_help()
		sys.exit()

	if not options.donor and not options.catalytic:
		parser.print_help()
		sys.exit()

	protein = Enzyme()
	sele = Selection()

	dmol = None
	for i in range(len(pdbfiles)):
		protein.readPDB(pdbfiles[i])
		#print pdbfiles[i]
		
		# --- get the donor --- #
		if options.donor:
			sele.makeSelection(options.donor)
			dmol = sele.apply_selection(protein)
			reslist = dmol.residueList()

			if len(reslist) != 1:
				#print "donor selection must specify one donor residue"
				#print reslist
				protein.clear()
				continue
				sys.exit()

			donor = reslist[0]
			sele.clear()
		elif options.catalytic:
			icat = int(options.catalytic) - 1
			donor = protein.catalytic[icat]
			if donor == None:
				print "can't find donor"
				sys.exit()


		# --- get the acceptor --- #
		sele.makeSelection(options.acceptor)
		amol = sele.apply_selection(protein)
		reslist = amol.residueList()
		sele.clear()
		
		if len(reslist) != 1:
			print "acceptor selection must specify one acceptor atom"
			sys.exit()

		if reslist[0].numAtoms() != 1:
			print "acceptor selection must specify one acceptor atom"
			sys.exit()

		acceptor = reslist[0].atom[0]

		# --- for now donor must be serine or tyrosine --- #
		if donor.name == "SER":
			H = donor.getAtom(" HG ")
			B = donor.getAtom(" OG ")
			C = donor.getAtom(" CB ")
			D = donor.getAtom(" CA ")
		elif donor.name == "TYR":
			H = donor.getAtom(" HH ")
			B = donor.getAtom(" OH ")
			C = donor.getAtom(" CZ ")
			D = donor.getAtom(" CE1")
		elif donor.name == "THR":
			H = donor.getAtom(" HG1")
			B = donor.getAtom(" OG1")
			C = donor.getAtom(" CB ")
			D = donor.getAtom(" CA ")
		elif donor.name == "CYS":
			H = donor.getAtom(" HG ")
			B = donor.getAtom(" SG ")
			C = donor.getAtom(" CB ")
			D = donor.getAtom(" CA ")
		else:
			print "unsupported donor residue"
			sys.exit()

		mytor = vector3d.torsion(acceptor.coord, B.coord, C.coord, D.coord)
		print pdbfiles[i], mytor
		#print mytor
#		changeDihedral(H,B,C,D,mytor)
		
#		protein.writePDB(outfiles[i], resRenumber=False, atomRenumber=False)
		protein.clear()
		if dmol != None:
			dmol.clear()


if __name__ == "__main__":
	main()

