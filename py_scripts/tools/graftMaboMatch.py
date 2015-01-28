#!/usr/bin/python


from Molecule import *
from ProteinLibrary import *
from optparse import OptionParser
import os, sys, string, re
from mol_routines import *
from match_routines import *
from file_routines import *



def main():

	"""
	changes a mabo-formatted file to a regular file
	"""
	
	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile",  help="outfile")
	parser.add_option("-O", dest="outlist",  help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
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

	mol = Molecule()
	cat = []
	for i in range(len(pdbfiles)):
		print pdbfiles[i]
		mol.readPDB(pdbfiles[i])
		print mol.numResidues()

		cat = getMaboCatResidues(mol, renumber=True)
		if len(cat) == 0:
			print "cant find mabo cat res"
			sys.exit()

		chainA = mol.getChain("A")
		if chainA == None:
			print "cannot find chain A"
			sys.exit()

		for res in cat:
			#print "-----"
			#print res
			chainA.replaceResidue(res.file_id,res)

		mol.removeChain("B")
		changeMaboHeader(mol)	
		chainA.renumber(resRenumber=False)
		mol.writePDB(outfiles[i],resRenumber=False,atomRenumber=False)
		mol.clear()

		


if __name__ == "__main__":
	main()
