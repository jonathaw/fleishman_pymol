#!/usr/bin/python


from Enzyme import *
from ProteinLibrary import *
from optparse import OptionParser
import os, sys, string, re
from mol_routines import *
from match_routines import *
from file_routines import *
from Loop_collection import *



def main():

	"""
takes output from a match run with flexible loops and grafts onto the scaffold
NOTE: deletes virtual atoms!!!
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-s", dest="scaffold", help="scaffold")
	parser.add_option("-o", dest="outfile",  help="outfile")
	parser.add_option("-O", dest="outlist",  help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-v", dest="virtual", help="virtual", action="store_true")
	parser.add_option("-l", dest="loop_lib", help="loob_library")
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
		outfiles = pdbfiles
	else:
		parser.print_help()
		sys.exit()

	if not options.scaffold:
		parser.print_help()
		sys.exit()

	if not options.loop_lib:
		parser.print_help()
		sys.exit()

	# setup in loop library	
	loop_lib = Loop_collection()
	loop_lib.read(options.loop_lib)

	scaffold = Molecule()
	scaffold.readPDB(options.scaffold)
	loop_lib.setNative(scaffold)

	
	mymatch = Enzyme()
	workMol = Molecule()
	re_flex = re.compile("REMARK FLEXIBLE LOOP")
	for i in range(len(pdbfiles)):
		mymatch.readPDB(pdbfiles[i])

		scaffold.clone(workMol)

		# graft in loops
		for rem in mymatch.remark:
			if re_flex.match(rem):
				cols = rem.split()
				resid  = int(cols[3])
				loopid = int(cols[5])

				myloop = loop_lib.getLoopLibrary(resid)
				if myloop == None:
					continue   # came from the scaffold
				else:
					newchain = myloop.getLoop(loopid-1)
					print myloop.start_point
					print myloop.end_point
					print workMol.chain[0].numResidues()
					workMol.chain[0].slice(myloop.start_point,myloop.end_point)
					workMol.chain[0].insertResidues(newchain.residue,myloop.start_point-1)
					workMol.chain[0].renumber()

		# graft over catalytic side chains
		for cat in mymatch.catalytic:
			workMol.chain[0].replaceResidue(int(cat.file_id),cat)

		ligchain = workMol.newChain()
		ligchain.addResidue(mymatch.ligand)

		virtualRes = Residue()
		if options.virtual:
			for virtualAtom in mymatch.virtualAtoms:
				virtualRes.addAtom(virtualAtom)
			ligchain.addResidue(virtualRes)
					
		workMol.remark = []
		workMol.remark = mymatch.remark
		workMol.writePDB(outfiles[i],resRenumber=False,atomRenumber=False)
		mymatch.clear()
		workMol.clear()

				
	
		


if __name__ == "__main__":
	main()
