#!/usr/bin/python

from optparse import OptionParser
import string, sys, os
from Molecule import *
from ResidueProperties import *



def main():

	"""
reports the statistics of residues involved in the protein-protein interface of
domain asssembly problems
	"""

	global cutoff, beg, end
	global protein, nres

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-l", dest="linker", help="linker")
	parser.add_option("-k", dest="domain_linker", help="domain_linker", action="store_true")
	parser.add_option("-d", dest="dump", help="dump", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()

	pdbfiles = []
	if options.pdblist:
		try:
			PDBLIST = open(options.pdblist)
		except:
			print "unable to open pdblist"
			sys.exit()

		for line in PDBLIST.readlines():
			line = string.strip(line)
			pdbfiles.append(line)
	elif options.pdbfile:
		pdbfiles.append(options.pdbfile)
	else:
		parser.print_help()
		sys.exit()
	
	if not options.linker:
		parser.print_help()
		sys.exit()

	do_dl = False
	do_dd = False
	if options.domain_linker:
		do_dl = True
	else:
		do_dd = True

	dump = False
	if options.dump:
		dump = True

	tmp = string.split(options.linker, "-")
	beg = int(tmp[0])
	end = int(tmp[1])

	cutoff = 8.0
	header = "pdbfile              #inter   #polar  #nonpolar  #aromatic  #charged"
	print header

	
	protein = Molecule()

	resline = ""
	for pdbfile in pdbfiles:
		protein.clear()
		protein.readPDB(pdbfile)
		nres = protein.numResidues()

		# find residues in interface between both domains
		if do_dd:
			domain_contacts = domain_domain_contacts()

		if do_dl:
			linker_contacts = domain_linker_contacts()

		props = ResidueProperties()
			
		if do_dd:
			dd_polar = []
			dd_nonpolar = []
			dd_aromatic = []
			dd_charged = []
			for atom in domain_contacts:
				resname = atom.parentResidue.name
				resid   = int(atom.parentResidue.file_id)
				if dump:
					resline += str(resid) + ","
				if resname in props.polar:
					dd_polar.append(atom)
				if resname in props.nonpolar:
					dd_nonpolar.append(atom)
				if resname in props.aromatic:
					dd_aromatic.append(atom)
				if resname in props.charged:
					dd_charged.append(atom)

				
		if do_dl:
			dl_polar = []
			dl_nonpolar = []
			dl_aromatic = []
			dl_charged = []
			for atom in linker_contacts:
				resname = atom.parentResidue.name
				resid   = int(atom.parentResidue.file_id)
				if dump:
					resline += str(resid) + ","
				if resname in props.polar:
					dl_polar.append(atom)
				if resname in props.nonpolar:
					dl_nonpolar.append(atom)
				if resname in props.aromatic:
					dl_aromatic.append(atom)
				if resname in props.charged:
					dl_charged.append(atom)

		# find interactions between domains and linkers 
		if do_dd:
			dd_response = ("%-20s %6i   %6i     %6i     %6i    %6i" % (pdbfile,\
				len(domain_contacts), len(dd_polar), len(dd_nonpolar), len(dd_aromatic),\
				len(dd_charged)))

		if do_dl:
			dl_response = ("%-20s %6i   %6i     %6i     %6i    %6i" % (pdbfile,\
				len(linker_contacts), len(dl_polar), len(dl_nonpolar), len(dl_aromatic),\
				len(dl_charged)))

		if do_dd:
			print dd_response

		if do_dl:
			print dl_response

		lr = len(resline)
		if dump:
			print resline[0:lr-1]


# ================================== #
# ===                            === #
# ===   domain_domain_contacts   === #
# ===                            === #
# ================================== #

def domain_domain_contacts():

	contact = []
	for chain in protein.chain:
		for i in range(beg-1):
			res1 = chain.residue[i]
			if res1.name != "GLY":
				centroid1 = res1.getAtom(" CB ")
			else:
				centroid1 = res1.getAtom(" CA ")

			if not centroid1:
				print "unable to locate centroid for residue:",i,res1.name
				sys.exit()

			
			for j in range(end+1,nres):
				res2 = chain.residue[j]
				if res2.name != "GLY":
					centroid2 = res2.getAtom(" CB ")
				else:
					centroid2 = res2.getAtom(" CA ")

				if not centroid2:
					print "unable to locate centroid for residue:",j,res2.name
					sys.exit()

				dist = centroid1.distance(centroid2)
				if dist < cutoff:
					bCentroid1 = False
					bCentroid2 = False

					for atom in contact:
						if centroid1 == atom:
							bCentroid1 = True

					for atom in contact:
						if centroid2 == atom:
							bCentroid2 = True

					if not bCentroid1:
						contact.append(centroid1)

					if not bCentroid2:
						contact.append(centroid2)

	return contact




# ================================== #
# ===                            === #
# ===   domain_linker_contacts   === #	
# ===                            === #
# ================================== #

def domain_linker_contacts():

	contacts = []
	for chain in protein.chain:
		for i in range(beg,end):
			res1 = chain.residue[i]
			
			if res1.name != "GLY":
				centroid1 = res1.getAtom(" CB ")
			else:
				centroid1 = res1.getAtom(" CA ")


			for j in range(1,beg-1):
				res2 = chain.residue[j]

				if res2.name != "GLY":
					centroid2 = res2.getAtom(" CB ")
				else:
					centroid2 = res2.getAtom(" CA ")

				dist = centroid1.distance(centroid2)
				if dist < cutoff:
					
					bCentroid = False
					for atom in contacts:
						if atom == centroid1:
							bCentroid = True

					if not bCentroid:
						contacts.append(centroid1)

			for j in range(end+1,nres):
				res2 = chain.residue[j]

				if res2.name != "GLY":
					centroid2 = res2.getAtom(" CB ")
				else:
					centroid2 = res2.getAtom(" CA ")

				dist = centroid1.distance(centroid2)
				if dist < cutoff:
					
					bCentroid = False
					for atom in contacts:
						if atom == centroid2:
							bCentroid = True

					if not bCentroid:
						contacts.append(centroid2)

	return contacts


if __name__ == "__main__":
	main()

