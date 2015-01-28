#!/usr/bin/python

from optparse import OptionParser
import sys, string
from Enzyme import *
from mol_routines import *
from file_routines import *
from match_routines import *


def main():

	"""
	program that checks to see if histidine binding to ligand is in the right place
	if not it switches the tautomer

	by default the proton is expected to be pointing AWAY from the ligand.
	this behaviour is changed with the -inverse option
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true")
	parser.add_option("-v", dest="virtual", help="virtual", action="store_true")
	parser.add_option("-c", dest="catalytic", help="catalytic")
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
	elif options.replace:
		for file in pdbfiles:
			outfiles.append(file)
	else:
		parser.print_help()
		sys.exit()

	if len(outfiles) != len(pdbfiles):
		print "differing number of files"
		sys.exit()


	mycat = None
	for i in range(len(pdbfiles)):
		#protein = Molecule()
		protein = Enzyme()
		protein.readPDB(pdbfiles[i])

		if options.catalytic:
			icat = int(options.catalytic) - 1
			if icat < 0 or icat >= len(protein.catalytic):
				print "accessing catalytic out of bounds"
				sys.exit()

			mycat = protein.catalytic[icat]

		chainB = extractCatResidues(protein)
		if len(chainB) == 0:
			print "NO CATALYTIC RESIDUES FOR",pdbfiles[i]
			sys.exit()	

		hislist = []
		for res in chainB:
			if res == None:
				print "missing catalytic residue"
				continue

			if res.name == "HIS":
				if mycat == None:
					hislist.append(res)
				elif res == mycat:
					hislist.append(res)
				#his = res

		if len(hislist) == 0:
			print "cannot find histidine in catalytic residues"
			sys.exit()

		for his in hislist:
			print his.file_id

			NDstate = True
			if his.atomExists(" HD1"):	
				proton = his.getAtom(" HD1")
			elif his.atomExists(" HE2"):
				proton = his.getAtom(" HE2")
				NDstate = False
			else:
				print "histidine is not protonated"
					
			hetlist = protein.getHeteroAtoms()
			mind = 1000.0
			for res in hetlist:
				cpres = res.clone()
				cpres.removeAtomsContaining("V")	
				dist = closestApproachToResidue(proton, cpres)
				mind = min(mind, dist)

			bPoint = False
			if mind < 4.0: 
				bPoint = True

			bChanged = False
			# --- if pointing and we don't want that: --- #
			if bPoint and not options.inverse:		
				switchHisTautomer(his)
				bChanged = True

			# --- if not pointing and we don't want that: --- #
			if not bPoint and options.inverse:
				switchHisTautomer(his)
				bChanged = True

			if bChanged:
				print "changed",pdbfiles[i]
				NDstate = not NDstate

			if options.virtual:
				hetatms = protein.getHeteroAtoms()
				for myres in hetatms:
					for atm in myres:
						if atm == None:
							break

						if atm.name == "VHNE":
							if not NDstate:
								atm.name = "VHND"
								continue

						if atm.name == "VHND":
							if NDstate:
								atm.name = "VHNE"
								continue
	
		protein.writePDB(outfiles[i], resRenumber=False, atomRenumber=False)	



if __name__ == "__main__":
	main()

