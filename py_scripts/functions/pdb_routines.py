#!/usr/bin/python

from Molecule import *

# ==================================================
# ===   changes X-ray seleno methionine to methionine
# ==================================================



def fixMet(mol=None):
	if mol == None:
		return

	for chain in mol.chain:
		for res in chain.residue:
			if res.name == "MSE":
				res.name = "MET"

				for atom in res.atom:
					atom.kind = "ATOM  "
					if atom.name == "SE  ":
						atom.name = " SD "

	

def aa1_from_num(num=0):
	if num == 1: return 'A'	
	if num == 2: return 'C'	
	if num == 3: return 'D'	
	if num == 4: return 'E'	
	if num == 5: return 'F'	
	if num == 6: return 'G'	
	if num == 7: return 'H'	
	if num == 8: return 'I'	
	if num == 9: return 'K'	
	if num == 10: return 'L'	
	if num == 11: return 'M'	
	if num == 12: return 'N'	
	if num == 13: return 'P'	
	if num == 14: return 'Q'	
	if num == 15: return 'R'	
	if num == 16: return 'S'	
	if num == 17: return 'T'	
	if num == 18: return 'V'	
	if num == 19: return 'W'	
	if num == 20: return 'Y'	
	return 'X'



def aa3_from_num(num=0):
	if num == 1: return 'ALA'	
	if num == 2: return 'CYS'	
	if num == 3: return 'ASP'
	if num == 4: return 'GLU'
	if num == 5: return 'PHE'
	if num == 6: return 'GLY'
	if num == 7: return 'HIS'
	if num == 8: return 'ILE'	
	if num == 9: return 'LYS'	
	if num == 10: return 'LEU'	
	if num == 11: return 'MET'	
	if num == 12: return 'ASN'	
	if num == 13: return 'PRO'	
	if num == 14: return 'GLN'	
	if num == 15: return 'ARG'	
	if num == 16: return 'SER'	
	if num == 17: return 'THR'	
	if num == 18: return 'VAL'	
	if num == 19: return 'TRP'	
	if num == 20: return 'TYR'	
	return 'XXX'



def num_from_aa1(res=""):
	if res == "A": return 1
	if res == "C": return 2
	if res == "D": return 3
	if res == "E": return 4
	if res == "F": return 5
	if res == "G": return 6
	if res == "H": return 7
	if res == "I": return 8
	if res == "K": return 9
	if res == "L": return 10
	if res == "M": return 11
	if res == "N": return 12
	if res == "P": return 13
	if res == "Q": return 14
	if res == "R": return 15
	if res == "S": return 16
	if res == "T": return 17
	if res == "V": return 18
	if res == "W": return 19
	if res == "Y": return 20
	return 0



def num_from_aa3(res=""):
	if res == "ALA": return 1
	if res == "CYS": return 2
	if res == "ASP": return 3
	if res == "GLU": return 4
	if res == "PHE": return 5
	if res == "GLY": return 6
	if res == "HIS": return 7
	if res == "ILE": return 8
	if res == "LYS": return 9
	if res == "LEU": return 10
	if res == "MET": return 11
	if res == "ASN": return 12
	if res == "PRO": return 13
	if res == "GLN": return 14
	if res == "ARG": return 15
	if res == "SER": return 16
	if res == "THR": return 17
	if res == "VAL": return 18
	if res == "TRP": return 19
	if res == "TYR": return 20
	return 0
