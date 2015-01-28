#!/usr/bin/python

from optparse import OptionParser
import sys, string
from Enzyme import *
from mol_routines import *
from file_routines import *
from Selection import *


def main():

	"""
checks whether the his-asp backup is syn or anti, or whether a glu is syn or anti to the ligand
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("--his_cat", dest="his_cat", help="catalytic histidine")
	parser.add_option("--asp_cat", dest="asp_cat", help="cataltyic asp or glu")
	parser.add_option("--lig_atm", dest="lig_atm", help="ligand atom")
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

	if not options.outfile:
		parser.print_help()
		sys.exit()

	if not options.asp_cat:
		parser.print_help()
		sys.exit()

	sele = Selection()
	if options.his_cat:
		his_cat = int(options.his_cat)-1
	elif options.lig_atm:
		sele.makeSelection(options.lig_atm)
	else:
		parser.print_help()
		sys.exit()

	try:
		OUTFILE = open(options.outfile,'w')
	except:
		print "unable to open outfile"
		sys.exit()

	protein = Enzyme()
	asp_cat = int(options.asp_cat)-1
	his_res = None
	asp_res = None

	O1  = None
	O2  = None
	COO = None
	HN  = None
	for i in range(len(pdbfiles)):
		protein.readPDB(pdbfiles[i])


		if asp_cat >= len(protein.catalytic):
			print "accessing asp/glu residue out of bounds"
			protein.clear()
			continue
		else:
			asp_res = protein.catalytic[asp_cat]

		# get atoms from asp/glu
		if asp_res.name == "ASP":
			O1  = asp_res.getAtom(" OD1")
			O2  = asp_res.getAtom(" OD2")
			COO = asp_res.getAtom(" CG ")
		elif asp_res.name == "GLU":
			O1  = asp_res.getAtom(" OE1")
			O2  = asp_res.getAtom(" OE2")
			COO = asp_res.getAtom(" CD ")

		if options.his_cat:
			if his_cat >= len(protein.catalytic):
				print "accessing histidine residue out of bounds"
				protein.clear()
				continue
			else:
				his_res = protein.catalytic[his_cat]

			# get atoms from his
			HN = his_res.getAtom(" HD1")
			if HN == None:
				HN = his_res.getAtom(" HE2")

		elif options.lig_atm:
			lig_list = sele.apply_selection(protein).atomList()
			if len(lig_list) != 1:
				print "ligand atom must specify 1 atom;",len(lig_list),"selected"
				sys.exit()

			HN = lig_list[0]

		if HN == None or O1 == None or O2 == None or COO == None:
			#print "unable to find appropriate atoms"
			protein.clear()
			continue

		# find closest HN-O distance
		nearbyO = O1
		otherO  = O2
		mindist = HN.distance(O1)
		dist = HN.distance(O2)
		if dist < mindist:
			mindist = dist
			nearbyO = O2
			otherO  = O1

		if mindist > 3.1:
			print pdbfiles[i],"no nearby oxygen found",mindist
			protein.clear()
			continue

		myang = vector3d.torsion(HN.coord,nearbyO.coord,COO.coord,otherO.coord)
		if myang < 90.0 and myang > -90.0:
			OUTFILE.write(pdbfiles[i]+" syn"+"\n")
		else:
			OUTFILE.write(pdbfiles[i]+" anti"+"\n")

		protein.clear()
		
	OUTFILE.close()


if __name__ == "__main__":
	main()

