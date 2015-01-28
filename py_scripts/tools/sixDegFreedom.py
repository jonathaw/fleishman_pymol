#!/usr/bin/python

from Molecule import *
from vector3d import *
from optparse import OptionParser
import sys, string
from file_routines import *


def main():

	"""
reports the catalytic six degrees of freedom between six atoms                 

order:    
LG1-LG2-LG3 ---- PR1-PR2-PR3
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-l", dest="lig_sele", help="ligand selection (atom numbers, comma delimited)")
	parser.add_option("-s", dest="prot_sele", help="protein selection (atom numbers, comma delimited)")
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

	if not options.lig_sele or not options.prot_sele:
		parser.print_help()
		sys.exit()

	# extract selections
	cols = options.lig_sele.split(",")
	if len(cols) != 3:
		print "ligand selection must specify 3 atoms.  You selected ",len(cols)
		sys.exit()

	lig_id = []
	for col in cols:
		lig_id.append(int(col))

	cols = options.prot_sele.split(",")
	if len(cols) != 3:
		print "protein selection must specify 3 atoms.  You selected ",len(cols)
		sys.exit()
		
	prot_id = []
	for col in cols:
		prot_id.append(int(col))

	protein = Molecule()
	print "pdbfile:                                  distAB   ang_A   tor_A   ang_B  tor_AB   tor_B"
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		alist = protein.atomList()

		lig_atoms = [-1]*3
		prot_atoms = [-1]*3
		for atm in alist:
			iatm = int(atm.file_id)

			for i in range(len(lig_id)):
				if iatm == lig_id[i]:
					lig_atoms[i] = atm

			for i in range(len(lig_id)):
				if iatm == prot_id[i]:
					prot_atoms[i] = atm

		if -1 in lig_atoms:
			print "cannot find 3 ligand atoms"
			sys.exit()

		if -1 in prot_atoms:
			print "cannot find 3 protein atoms"
			sys.exit()

		distAB = lig_atoms[2].distance(prot_atoms[0])
		ang_a  = vector3d.angle3(lig_atoms[1].coord,lig_atoms[2].coord,prot_atoms[0].coord)
		ang_b  = vector3d.angle3(lig_atoms[2].coord,prot_atoms[0].coord,prot_atoms[1].coord)
		tor_a  = vector3d.torsion(lig_atoms[0].coord,lig_atoms[1].coord,lig_atoms[2].coord,prot_atoms[0].coord)
		tor_b  = vector3d.torsion(lig_atoms[2].coord,prot_atoms[0].coord,prot_atoms[1].coord,prot_atoms[2].coord)
		tor_ab = vector3d.torsion(lig_atoms[1].coord,lig_atoms[2].coord,prot_atoms[0].coord,prot_atoms[1].coord)

		id1 = int(prot_atoms[0].file_id)
		id2 = int(prot_atoms[1].file_id)
		id3 = int(prot_atoms[2].file_id)
		print "%-28s%4i%4i%4i%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f" % (pdbfile,id1,id2,id3,distAB,ang_a,tor_a,ang_b,tor_ab,tor_b)
				
		protein.clear()
		



if __name__ == "__main__":
	main()

