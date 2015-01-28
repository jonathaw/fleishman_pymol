#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Enzyme import *
from Resfile import *
from file_routines import *
from mol_routines import *
from ss_routines import *

def main():

	"""
creates a resfile from an enzyme.  Redesigned positions are chosen based on their
distance from the ligand and catalytic residues.
By default GLY and PRO positions are unaltered
	"""

	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-a", dest="auto",    help="auto_resfile", action="store_true")
	parser.add_option("-n", dest="native",  help="native")
	parser.add_option("--mut_gly_pro",      dest="keep", help="allow gly and pro to be mutated", action="store_true")
	parser.add_option("--no_ss_gly",        dest="no_ss_gly", help="no glycine at ss", action="store_true")
	parser.add_option("--restrict_non_native", dest="restrict_non_native", help="restrict non native residues")
	parser.add_option("--restrict_all",      dest="restrict_all", help="restrict these amino acid types")
	parser.add_option("--force_mutation",    dest="force_mutation", help="force mutation")
	parser.add_option("--keep_nonpolar",     dest="keep_nonpolar", help="keeps nonpolar residues non-polar", action="store_true")
	parser.add_option("--repack_only",       dest="repack_only", help="repack only", action="store_true")
	parser.add_option("--repack_catalytic",  dest="repack_catalytic", help="repack catalytic", action="store_true")
	parser.add_option("--ligand_shell_only", dest="ligand_shell_only", help="ligand shell only", action="store_true")
	parser.add_option("--shell1_cutoff",     dest="shell1_cutoff", help="shell 1 cutoff (7.0)", default=7.0)
	parser.add_option("--shell2_cutoff",     dest="shell2_cutoff", help="shell 2 cutoff (9.0)", default=9.0)
	parser.add_option("--shell3_cutoff",     dest="shell3_cutoff", help="shell 3 cutoff (11.0)", default=11.0)
	parser.add_option("--shell1_allow",      dest="shell1_allow",  help="allowed residues in shell1")
	parser.add_option("--shell1_restrict",   dest="shell1_restrict", help="restricted residues in shell1")
	parser.add_option("--shell1_restrict_non_native", dest="shell1_restrict_non_native", help="restricted non-native residues in shell1")
	parser.add_option("--shell2_allow",      dest="shell2_allow",  help="allow residues in shell2")
	parser.add_option("--shell2_restrict",   dest="shell2_restrict", help="restricted residues in shell2")
	parser.add_option("--shell2_restrict_non_native", dest="shell2_restrict_non_native", help="restricted non-native residues in shell2")
	parser.add_option("--verbose",           dest="verbose", help="verbose", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()


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
	elif options.auto:
		for file in pdbfiles:
			base = get_basefile(file)
			file2 = base + ".resfile"
			outfiles.append(file2)
	else:
		parser.print_help()
		sys.exit()

	nfiles = len(pdbfiles)
	if len(outfiles) != nfiles:
		print "number of files differ"
		parser.print_help()
		sys.exit()
		
	
	enz = Enzyme()
	resfile = Resfile()
	for ifile in range(nfiles):
		enz.clear()
		resfile.clear()

		print pdbfiles[ifile]

		enz.readPDB(pdbfiles[ifile])

		# make sure that catalytic residues were read in
		if len(enz.catalytic) == 0:
			continue

		resfile.setMolecule(enz)

		# get secondary structure if necessary
		if options.no_ss_gly:
			natss = getSecondaryStructure(pdbfiles[ifile])
			if len(natss) < enz.protein.numResidues():
				print "number of residues and secondary structure do no match"
				sys.exit()


		prot = enz.protein	
		lig  = enz.ligand
		nres = len(prot.residue)

		designable = [False]*nres
		repackable = [False]*nres

		in_shell1 = [False]*nres
		in_shell2 = [False]*nres

		for i in range(nres):
			res = prot.residue[i]
			if enz.isCatalytic(res):
				if options.repack_catalytic:
					repackable[i] = True
				else:
					resfile.setCatalytic(i)
			else:
				CB = None
				if res.name == "GLY":
					CB = res.getAtom(" CA ")
				else:
					CB = res.getAtom(" CB ")

				if CB == None:
					continue
				

				# --- get distance to ligand --- #
				distCB = closestApproachToResidue(CB,lig)
				if distCB < float(options.shell1_cutoff):
					designable[i] = True
					in_shell1[i]  = True
				elif distCB < float(options.shell2_cutoff):
					if isResPointingToRes(res, lig, cutoff=60):
						designable[i] = True
						in_shell2[i]  = True
					else:
						repackable[i] = True
				elif distCB < float(options.shell3_cutoff):
					repackable[i] = True

				
				# --- get distance to catalytic residues if necessary
				if not options.ligand_shell_only:
					focusedRes = None
					mindist = 5000
					if not designable[i]:
						for cres in enz.catalytic:
							print cres
							dist = closestApproachToResidue(CB, cres)
							if dist < mindist:
								focusedRes = cres
								mindist = dist

						if focusedRes != None:
							if mindist < float(options.shell1_cutoff):
								if isResPointingToRes(res, focusedRes, cutoff=60):
									in_shell1[i] = True
									designable[i] = True
								else:
									repackable[i] = True
							elif mindist < float(options.shell2_cutoff):
								repackable[i] = True

		allAA = "ACDEFGHIKLMNPQRSTVWY"
		polar = "EDSTNQHKR"
		nonpolar = "ACFGILMPVWY"

		# ---   if restricting non native residues, get the native sequence   --- #
		natseq = enz.sequence()
		if options.restrict_non_native:
			if options.native:
				natpdb = Enzyme()
				natpdb.readPDB(options.native)
				natseq = natpdb.sequence()
				natpdb.clear()


		allAApos = allAA
		forced_mutations = []
		if options.force_mutation:
			cols = options.force_mutation.split(",")
			for col in cols:
				forced_mutations.append(int(col)-1)


		for i in range(nres):
			res = enz.protein.residue[i]

			if options.verbose:
				if repackable[i]:
					print i+1,res.name,"repackable"
				elif designable[i]:
					if in_shell1[i]:
						print i+1,res.name,"shell1"
					elif in_shell2[i]:
						print i+1,res.name,"shell2"

			if repackable[i]:
				if i in forced_mutations:
					designable[i] = True
				else:
					resfile.repackOnly(i)

			if not designable[i] and not repackable[i]:
				if i in forced_mutations:
					designable[i] = True

			# ---   keep gly and pro at designable positions   --- #
			if designable[i]:
				if not options.keep:
					#if res.name == "GLY":
					if natseq[i] == "G":
						resfile.designResidue(i,"G")
						continue
					elif natseq[i] == "P":
						resfile.designResidue(i,"P")
						continue

			if designable[i]:
				if options.repack_only:
					resfile.repackOnly(i)
					continue

				resfile.designResidue(i,allAA)

				# shell info
				if options.shell1_allow:
					if in_shell1[i]:
						resfile.designResidue(i,options.shell1_allow)
				if options.shell1_restrict: 
					if in_shell1[i]:
						resfile.restrictBy(i,options.shell1_restrict)
				if options.shell1_restrict_non_native:
					if in_shell1[i]:
						resfile.restrictBy(i,options.shell1_restrict_non_native)
						resfile.expandBy(i, res.aa1())

				if options.shell2_allow:
					if in_shell2[i]:
						resfile.designResidue(i,options.shell2_allow)
				if options.shell2_restrict:
					if in_shell2[i]:
						resfile.restrictBy(i,options.shell2_restrict)
				if options.shell2_restrict_non_native:
					if in_shell2[i]:
						resfile.restrictBy(i,options.shell2_restrict_non_native)
						resfile.expandBy(i, res.aa1())

				# restrict polar groups
				if options.keep_nonpolar:
					if natseq[i] in nonpolar:
						resfile.restrictBy(i,polar)

				# restrict the types of non-native amino acids
				if options.restrict_non_native:
					resfile.restrictBy(i, options.restrict_non_native)
					resfile.expandBy(i, res.aa1())

				# restrict glycine at secondary structure positions
				if options.no_ss_gly:
					if natss[i] == "H" or natss[i] == "E":
						resfile.restrictBy(i, "G")

				# restrict amino acid types at all positons
				if options.restrict_all:
					resfile.restrictBy(i, options.restrict_all)

				# force a mutation
				if i in forced_mutations:
					print "restricting",i+1,"by",natseq[i]
					resfile.restrictBy(i,natseq[i])


					
						
		resfile.write(outfiles[ifile])




if __name__ == "__main__":
	main()
