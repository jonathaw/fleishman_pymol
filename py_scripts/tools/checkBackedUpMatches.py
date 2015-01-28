#!/usr/bin/python


from Molecule import *
from ProteinLibrary import *
from InteractionGraph import *
from Selection import *
from optparse import OptionParser
import os, sys, string, re
from mol_routines import *



def main():

	"""
	Given a list of regular matches and a list of possible backed up positions
	all combinations of backed up residues are generated
	"""
	
	parser = OptionParser()
	parser.add_option("-m", dest="match_log", help="match log")
	parser.add_option("-b", dest="bkup_log", help="bkup log")
	parser.add_option("-g", dest="interaction_graph", help="interaction graph")
	parser.add_option("-s", dest="silent", help="no output files", action="store_true")
	parser.add_option("-f", dest="force", help="force output", action="store_true")
	parser.add_option("-l", dest="limit", help="limit output", action="store_true")
	parser.add_option("-i", dest="ignore", help="ignore clash check (SC or LIG or ALL)")
	parser.add_option("-t", dest="triad", help="triad log", action="store_true")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()


	if not options.match_log or not options.bkup_log or not options.interaction_graph:
		parser.print_help()
		sys.exit()


	# ---  get rotamers from match log   --- #
	re_ig = re.compile("InteractionGraph match")	
	bk_ig = re.compile("New value for \[-backed_up_residue\]")
	ct_ig = re.compile("REMARK BACKBONE TEMPLATE A ")
	
	try:
		LOG = open(options.match_log)
	except:
		print "unable to open match log file"
		sys.exit()

	match_file = []
	match_rot = []
	bk_res = -1
	for line in LOG:
		if re_ig.match(line):
			cols = line.split()
			match_file.append(cols[6])
			match_rot.append(int(cols[3]))

		if bk_ig.search(line):
			cols = line.split()
			bk_res = int(cols[5])

	LOG.close()
	if bk_res == -1:
		print "ERROR: cannot determine backed up residue from log file"
		sys.exit()
	bk_res = bk_res -1


	# ---   get rotamers from backed up log   --- #
	try:
		BLOG = open(options.bkup_log)
	except:
		print "unable to open backup log file"
		sys.exit()

	bkup_file = []
	bkup_rot = []
	for line in BLOG:
		if re_ig.match(line):
			cols = line.split()
			bkup_file.append(cols[6])
			bkup_rot.append(int(cols[3]))

	BLOG.close()
	


	mychain = Selection()
	mychain.makeSelection("chain=B")

	# ---   check for backed up rotamers   --- #
	IG = InteractionGraph()
	IG.read(options.interaction_graph)
	IG.sortEnergies()

	n_match_rots = len(match_rot)
	target = Molecule()
	probe = Molecule()
	npass = 0
	scale = 0.75
	lig_scale = 0.85

	printTriad = True
	for i in range(n_match_rots):
		print match_rot[i],match_file[i],":"
		ccc  = match_file[i].split("./")
		if len(ccc) > 1:
			dafile = ccc[1]
		else:
			dafile = match_file[i]
		cols = dafile.split(".")
		basename = cols[0]
		
		partners = IG.get_rotamer_partners(match_rot[i])

		# --- extract chain B residues and hetero atoms --- #
		target.readPDB(match_file[i])
		if target.numResidues() == 0:
			continue

		tarB = mychain.apply_selection(target)
		reslist = tarB.residueList()
		npos = len(reslist) + 1
		if bk_res < 0 or bk_res >= len(reslist):
			print "accessing backed up residue out of bounds"
			sys.exit()

		# get corrected catatlytic residue id's
		cat_id = []
		tmp_cat = []
		tmp_id = []
		for rem in target.remark:
			if ct_ig.match(rem):
				cols = rem.split()
				tmp_cat.append(int(cols[10]))
				tmp_id.append(int(cols[11]))

		for i in range(len(tmp_id)):
			for j in range(len(tmp_id)):
				if tmp_id[j] == i+1:
					cat_id.append(tmp_cat[j])

		if options.triad:
			if printTriad:
				print "[INT  OPT]New value for [-backed_up_residue]",(len(cat_id)+1)
				printTriad = False

		hetlist = target.getHeteroAtoms()
		prtnr_found = False

		prtnr_seen = {}
		for prtnr in partners:
			if not prtnr in bkup_rot:
				continue

			prtnr_found = True

			j = bkup_rot.index(prtnr)
			print "   ",bkup_file[j],
			probe.readPDB(bkup_file[j])	
			if probe.numResidues() == 0:
				continue

			chainB = probe.getChain("B")
			probe_sc = chainB.residue[0]
			probe_pos = IG.get_rotamer(prtnr).seqpos

			failed = False

			# just check that we're not placing a backed up reside on top of another catalytic residue
			if int(probe_pos) in cat_id:
				print "FAIL (placement)",probe_pos
				failed = True

			# --- check for clashes with the ligand --- #
			if options.ignore != "LIG" and options.ignore != "ALL":
				if not failed:
					for hetres in hetlist:
						if (bResidue_Residue_clash_check(hetres, probe_sc, lig_scale)):
							print "FAIL (LIG)"
							failed = True
							break

			# --- check for clashes with other side chains --- #
			if options.ignore != "SC" and options.ignore != "ALL":
				if not failed:
					for res in reslist:
						if (bResidue_Residue_clash_check(res, probe_sc, scale)):
							print "FAIL (SC-" + res.name + str(res.file_id) + ")"
							failed = True
							break


			if not failed or options.force:
				if options.limit:
					if int(probe_pos) in prtnr_seen.keys():
						print "SKIPPING"
						probe.clear()
						continue

				npass += 1
				print "PASS"
				prtnr_seen[int(probe_pos)] = 1
				if not options.silent:
					# ---   output pdbfile   --- #
					outname = basename + "_" + str(prtnr) + "_bk.pdb"
					outmol = target.clone()
					tchainB = outmol.getChain("B")
					probe_sc.file_id = probe_pos
					tchainB.addResidue(probe_sc)
					#probe_remark = "REMARK ROSETTA_MATCH TEMPLATE A " + probe_sc.name + ("%4s" % probe_pos) + " MATCH MOTIF B " + probe_sc.name + str(probe_sc.file_id)
					probe_remark = "REMARK BACKBONE TEMPLATE A " + reslist[bk_res].name + ("%5i" % cat_id[bk_res]) + " MATCH MOTIF B " + probe_sc.name + ("%6i" % int(probe_sc.file_id)) + ("%3i" % npos)
					outmol.addRemark(probe_remark)
					outmol.writePDB(outname, resRenumber=False, atomRenumber=False)
					outmol.clear()

					if options.triad:
						print "InteractionGraph match: rotamer",str(prtnr),"used for",outname

				#if options.limit:         # only output best combination
			#		probe.clear()
			#		break
					

			probe.clear()

		if not prtnr_found:
			print "   NO PARTNER!"

		target.clear()

	print "\n\n================================"
	print "number of structures passing =",npass
	print "================================="
		



if __name__ == "__main__":
	main()

