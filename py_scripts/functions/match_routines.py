#!/usr/bin/python

from Molecule import *
import commands, os, sys, string, re



def changeMaboHeader(mol=None):

	"""
	changes the header of a match from Mabo formatted to default type
	"""

	if mol == None:
		return

	temp = re.compile("ROSETTA_MATCH TEMPLATE A")
	newrem = []
	nrem = 1
	for rem in mol.remark:
		if temp.search(rem):
			cols = rem.split()
			line = "REMARK BACKBONE TEMPLATE A " + cols[4] + ("%5s" % cols[5]) + " MATCH MOTIF B " + cols[9][0:3] + ("%6i%3i" % (nrem, nrem))
			newrem.append(line)
			nrem += 1

	mol.remark = newrem



def extractCatResidues(mol=None):

	"""
	extracts catalytic residues checking for mabo or non-mabo formats
	"""	

	cat = getMaboCatResidues(mol)
	#print len(cat)
	if len(cat) == 0:
		cat = getCatalyticResidues(mol)
		return cat
	else:
		return cat



def getMaboCatResidues(mol=None, renumber=False):

	"""
	extracts the catalytic residues from a matched pdbfile
	(in mabo format)
	if renumber, then put the proper residue id in the sidechain
	"""

	cat = []
	if mol == None:
		return cat

	temp = re.compile("ROSETTA_MATCH TEMPLATE A")
	found = False
	for rem in mol.remark:
		if temp.search(rem):
			found = True

	if not found:
		return cat

	chainB = mol.getChain("B")
	if not chainB:
		print "cannot find chain B"
		return cat

	cat = chainB.residue
	ncat = len(cat)
	if ncat == 0:
		print "no catalytic residues present"
		return cat

	
	if renumber:
		temp = re.compile("ROSETTA_MATCH TEMPLATE A")
		nres = 0
		for rem in mol.remark:
			if temp.search(rem):
				if nres >= ncat:
					print "not enough catalytic residues"
					cat = []
					return cat					

				cols = rem.split()
				resi = cols[5]
				cat[nres].file_id = resi
				nres += 1
	return cat
			
		

def getCatalyticResidues(mol=None):

	"""
	extracts the catalytic residues from a matched pdbfile
	(not in mabo format)
	"""

	cat = []
	if mol == None:
		return cat
		
	temp = re.compile("REMARK BACKBONE TEMPLATE")
	temp1 = re.compile("REMARK   0 BONE TEMPLATE")
	lg1  = re.compile("LG1")
	chainA = mol.chain[0]
	if not chainA:
		print "cannot find chain A"
		return cat

	newformat = False
	for rem in mol.remark:
		if lg1.search(rem):
			newformat = True
			
		
	for rem in mol.remark:
		if temp.search(rem) or temp1.search(rem):
			cols = rem.split()	
			#chn = cols[3]
			#res  = cols[5]
			if newformat:
				res = cols[10]
			else:
				res = cols[5]
			#mychn = mol.getChain(chn)
			mychn = mol.chain[0]
			if mychn == None:
				continue
			#cres = mol.getChain(chn).getResidue(res)
			cres = mychn.getResidue(res)
			cat.append(cres)

	return cat



def getCatalyticResidue(mol=None, ires=-1):

	"""
	extracts the catalytic residues from a matched pdbfile
	(not in mabo format)
	"""

	cres = None
	if mol == None:
		return cres

	if ires == -1:
		return cres

		
	temp = re.compile("REMARK BACKBONE TEMPLATE")
	chainA = mol.getChain("A")
	if not chainA:
		chainA = mol.chain[0]

	if chainA == None:
		print "cannot find chain A"
		return cres
		
	for rem in mol.remark:
		cols = rem.split()	
		if int(cols[11]) == ires:
			res  = cols[5]
			cres = chainA.getResidue(res)

	return cres



def getCatalyticResidueList(mol=None):

	"""
	extracts the catalytic residues from a matched pdbfile
	(not in mabo format)
	returns a list of residue id's
	"""

	cat = []
	if mol == None:
		return cat
		
	temp = re.compile("REMARK BACKBONE TEMPLATE")
	chainA = mol.getChain("A")
	if not chainA:
		print "cannot find chain A"
		return cat
		
	for rem in mol.remark:
		cols = rem.split()	
		res  = cols[5]
		cat.append(int(res))

	return cat
