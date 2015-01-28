#!/usr/bin/python

from Molecule import *
from Builder import *
import commands, os, sys, string, re, math

# ==================================================
# ===   rotates a molecule given a rotation matrix
# ==================================================


_rosetta_type = {}
_rosetta_type["aroC"] = "C"
_rosetta_type["Nhis"] = "N"
_rosetta_type["OCbb"] = "O"
_rosetta_type["COO "] = "C"
_rosetta_type["OOC "] = "O"
_rosetta_type["Haro"] = "H"
_rosetta_type["Hapo"] = "H"
_rosetta_type["CH3 "] = "C"
_rosetta_type["CH1 "] = "C"
_rosetta_type["CH2 "] = "C"
_rosetta_type["Npro"] = "N"
_rosetta_type["CNH2"] = "C"
_rosetta_type["OH  "] = "O"
_rosetta_type["NH2O"] = "N"
_rosetta_type["ONH2"] = "O"
_rosetta_type["Hpol"] = "H"
_rosetta_type["HOH "] = "O"


def rotate_molecule(mol=None,mat=None):
	if mol == None or mat == None:
		return

	s = [None]*3
	v = [None]*3

	for chain in mol.chain:
		for res in chain.residue:
			for atm in res.atom:
				s[0] = atm.coord.x
				s[1] = atm.coord.y	
				s[2] = atm.coord.z

				v[0] = 0.0
				v[1] = 0.0
				v[2] = 0.0

				for j in range(3):
					for k in range(3):
						v[j] += s[k]*mat[k][j]

				atm.coord.x = v[0]
				atm.coord.y = v[1]
				atm.coord.z = v[2]



def rotateArbitraryAxis(mol=None, vec=None, ang=None):

	"""
	rotates a molecule about an arbitrary axis
	"""

	if mol == None or vec == None or ang == None:
		print "Usage: rotateArbitraryAxis(mol, vec, angle)"
		sys.exit()

	vec = vec.unit()

	l  = vec.length()
	l2 = vec.length2()

	u = vec.x
	v = vec.y
	w = vec.z

	ang = ang/57.2957795

	mat = [None]*3
	for i in range(len(mat)):
		mat[i] = [None]*3

	ca = math.cos(ang)
	sa = math.sin(ang)

	mat[0][0] = u*u*(1-ca) + ca
	mat[1][0] = u*v*(1-ca) - w*sa
	mat[2][0] = u*w*(1-ca) + v*sa

	mat[0][1] = u*v*(1-ca) + w*sa
	mat[1][1] = v*v*(1-ca) + ca
	mat[2][1] = v*w*(1-ca) - u*sa

	mat[0][2] = u*w*(1-ca) - v*sa
	mat[1][2] = v*w*(1-ca) + u*sa
	mat[2][2] = w*w*(1-ca) + ca

	rotate_molecule(mol, mat)



def rotateAboutAxis(mol=None, axis=None, ang=None):

	"""
	specify the axis to rotate about
	"""

	if mol == None or axis == None or ang == None:
		print "usage: rotateAbouxAxis(mol, axis, ang)"
		return

	if axis == "x" or axis == "X":
		rotateAboutX(mol, ang)
		return
	if axis == "y" or axis == "Y":
		rotateAboutY(mol, ang)
		return
	if axis == "z" or axis == "Z":
		rotateAboutZ(mol, ang)
		return

	print "unrecognized axis |" + axis + "|"


def rotateAboutX(mol=None, ang=90.0):

	"""
	rotates a vector about the x-axis by a given angle
	"""

	ang = ang/57.2957795

	mat = [None]*3
	for i in range(len(mat)):
		mat[i] = [None]*3

	mat[0][0] = 1.0
	mat[0][1] = 0.0
	mat[0][2] = 0.0

	mat[1][0] = 0.0
	mat[1][1] = math.cos(ang)
	mat[1][2] = math.sin(ang)

	mat[2][0] = 0.0
	mat[2][1] = -math.sin(ang)		
	mat[2][2] = math.cos(ang)

	rotate_molecule(mol, mat)

				
def rotateAboutZ(mol=None, ang=90.0):

	"""
	rotates a vector about the x-axis by a given angle
	"""

	ang = ang/57.2957795

	mat = [None]*3
	for i in range(len(mat)):
		mat[i] = [None]*3

	mat[0][0] = math.cos(ang)
	mat[0][1] = math.sin(ang)
	mat[0][2] = 0.0

	mat[1][0] = -math.sin(ang)
	mat[1][1] = math.cos(ang)
	mat[1][2] = 0.0

	mat[2][0] = 0.0
	mat[2][1] = 0.0
	mat[2][2] = 1.0

	rotate_molecule(mol, mat)



def rotateAboutY(mol=None, ang=90.0):

	"""
	rotates a vector about the y-axis by a given angle
	"""

	ang = ang/57.2957795

	mat = [None]*3
	for i in range(len(mat)):
		mat[i] = [None]*3

	mat[0][0] = math.cos(ang)
	mat[0][1] = 0.0
	mat[0][2] = -math.sin(ang)

	mat[1][0] = 0.0
	mat[1][1] = 1.0
	mat[1][2] = 0.0

	mat[2][0] = math.sin(ang)
	mat[2][1] = 0.0
	mat[2][2] = math.cos(ang)

	rotate_molecule(mol, mat)



def superimpose_molecule(trg=None,prb=None,carry=None):
	if trg == None or prb == None:
		return

	if trg.numAtoms() != prb.numAtoms():
		print "superimpose_molecule: number of atoms differ"
		return

	trg_com = trg.com()
	prb_com = prb.com()
	prb_com = -prb_com

	tmp_target = "_trg"
	tmp_probe  = "_prb"

	trg.writePDB(tmp_target)
	prb.writePDB(tmp_probe)
	
	t = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
	output = commands.getoutput("superimpose " + tmp_target + " " + tmp_probe)
	outlines = output.split("\n")

	cols1 = outlines[1].split()
	cols2 = outlines[2].split()
	cols3 = outlines[3].split()

	cols4 = outlines[5].split()

	t[0][0] = float(cols1[0]); t[0][1] = float(cols1[1]); t[0][2] = float(cols1[2])
	t[1][0] = float(cols2[0]); t[1][1] = float(cols2[1]); t[1][2] = float(cols2[2])
	t[2][0] = float(cols3[0]); t[2][1] = float(cols3[1]); t[2][2] = float(cols3[2])

	if carry != None:
		carry.translate(prb_com)		
		rotate_molecule(carry, t)
		carry.translate(trg_com)
	else:
		prb.translate(prb_com)
		rotate_molecule(prb, t)
		prb.translate(trg_com)

	commands.getoutput("rm -f " + tmp_target)
	commands.getoutput("rm -f " + tmp_probe)

	return float(cols4[2])



def mammoth(targetFile="", probeFile="", Rvalue=4.0):
	if targetFile == "" or probeFile == "":
		return

	mam_results = "_mammoth"
	exe = "mammoth -e " + targetFile + " -p " + probeFile + " -o " + mam_results + " -R " + str(Rvalue)
	ans = commands.getoutput(exe)

	try:
		PDB = open("maxsub_sup.pdb", 'r')
	except:
		print "unable to open maxsub"
		return
			
	tmat = re.compile("REMARK Transformation Matrix")			
	pvec = re.compile("Prediction")
	evec = re.compile("Experiment")
	rms  = re.compile("RMS")
	psi  = re.compile("PSI")

	readT = False
	readPV = False
	readEV = False
	n = 0
	matrix = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
	vectorP = vector3d()
	vectorE = vector3d()
	for line in PDB.readlines():
		line = string.rstrip(line)

		if rms.search(line):
			cols = line.split()
			rmsvalue = cols[3]

		if psi.search(line):
			cols = line.split()
			psivalue = cols[2]

		if tmat.search(line):
			readT = True	
			continue

		if pvec.search(line):
			readPV = True
			continue

		if evec.search(line):
			readEV = True
			continue

		if readT:
			if n == 3:
				readT = False
				continue

			cols = line.split()
			matrix[n][0] = float(cols[1])
			matrix[n][1] = float(cols[2])
			matrix[n][2] = float(cols[3])
			n += 1
		
		if readPV:
			cols = line.split()
			readPV = False
			vectorP[0] = float(cols[1])
			vectorP[1] = float(cols[2])
			vectorP[2] = float(cols[2])

		if readEV:
			cols = line.split()
			readEV = False
			vectorE[0] = float(cols[1])
			vectorE[1] = float(cols[2])
			vectorE[2] = float(cols[2])

	vectorP = -vectorP
	probe = Molecule()
	target = Molecule()
	probe.readPDB(probeFile)
	target.readPDB(targetFile)
	pcom = probe.com()
	pcom = -pcom
	tcom = target.com()
	probe.translate(pcom)
	#probe.translate(vectorP)
	rotate_molecule(probe, matrix)
	#probe.translate(vectorE)
	probe.translate(tcom)
	PDB.close()

	return [probe, psivalue, rmsvalue]



def fit(mol1=None, mol2=None):
	if mol1 == None or mol2 == None:
		print "usage: fit(mol1,mol2)"
		return

	# make sure that both molecules have the same number of atoms and residues
	nRes = mol1.numResidues()
	if mol2.numResidues() != nRes:
		print "molecules have different number of residues"
		return 

	if mol1.numAtoms() != mol2.numAtoms():
		print "molecules have different number of atoms"
		return
	
	rmsd = 0.0
	nAt  = 0
	for ic in range(mol1.numChains()):
		chain1 = mol1.chain[ic]
		chain2 = mol2.chain[ic]

		nRes = chain1.numResidues() 
		for ires in range(nRes):
			res1 = chain1.residue[ires]
			res2 = chain2.residue[ires]

			nAtom = res1.numAtoms()
			for iatom in range(nAtom):
				atom1 = res1.atom[iatom]
				atom2 = res2.atom[iatom]

				rmsd += atom1.dist2(atom2)
				nAt  += 1

	rmsd /= float(nAt)
	rmsd = math.sqrt(rmsd)

	return rmsd
	


def res_fit(mol1=None, mol2=None):
	if mol1 == None or mol2 == None:
		print "usage: fit(mol1,mol2)"
		return

	# make sure that both molecules have the same number of atoms and residues
	nRes = mol1.numResidues()
	if mol2.numResidues() != nRes:
		print "molecules have different number of residues"
		return 

	if mol1.numAtoms() != mol2.numAtoms():
		print "molecules have different number of atoms"
		return
	
	nAt  = 0
	result = []
	for ic in range(mol1.numChains()):
		chain1 = mol1.chain[ic]
		chain2 = mol2.chain[ic]

		nRes = chain1.numResidues() 
		for ires in range(nRes):
			res1 = chain1.residue[ires]
			res2 = chain2.residue[ires]

			nAtom = res1.numAtoms()
			nAt = 0
			rmsd = 0.0
			for iatom in range(nAtom):
				atom1 = res1.atom[iatom]
				atom2 = res2.atom[iatom]

				rmsd += atom1.dist2(atom2)
				nAt  += 1

			rmsd /= float(nAt)
			rmsd = math.sqrt(rmsd)
			result.append((res1.file_id,rmsd))

	return result



def bondedNeighbors(res=None, atm=None, cutoff=2.0):

	"""
	checks connectivities within a residue
	"""

	if res == None or atm == None:
		return

	neigh = []
	for n in res.atom:
		if n != atm:
			if atm.distance(n) < cutoff:
				neigh.append(n)

	return neigh



def fitAtomList(list1=None, list2 = None):

	"""
	returns the rms for two lists of atoms
	"""

	nAt = len(list1)
	if nAt != len(list2):
		print "size of lists differ"
		sys.exit()

	rmsd = 0.0
	for i in range(nAt):
		rmsd += list1[i].dist2(list2[i])

	rmsd /= float(nAt)
	rmsd = math.sqrt(rmsd)

	return rmsd



def bAtom_Atom_clash_check(atm1=None, atm2=None,scale=0.95):
	
	"""
	checks for clashes between two atoms where a clash is defined when
	two atoms come closer than the sum of their radii
	"""

	# --- check to see that atoms have a defined element
	if atm1.radius < 0.05 or atm2.radius < 0.05:
		return False


	dist = atm1.distance(atm2)
	if dist < scale*(atm1.radius + atm2.radius):
		#print "clash between:"
		#print atm1
		#print atm2
		#print "distance = ",dist
		#print "combined radii = ",(atm1.radius+atm2.radius)
		return True

	return False



def bResidue_Residue_clash_check(res1=None, res2=None, scale=0.95):

	"""
	checks for clashes between atoms in residue 1 and residue 2
	"""

	for atm1 in res1.atom:
		for atm2 in res2.atom:
			if bAtom_Atom_clash_check(atm1, atm2, scale):
				return True

	return False
			


def switchHisTautomer(his=None):
	
	"""
	switches the histidine tautomer by changing the HNE to a HND or vice versa
	takes in a residue object
	"""

	if his.name != "HIS":
		return

	billder = Builder()
	# --- check to see if it's an HID or HIE --- #
	if his.atomExists(" HE2"):
		H = his.getAtom(" HE2")
		A = his.getAtom(" ND1")
		B = his.getAtom(" CG ")
		C = his.getAtom(" CD2")
		name = " HD1"
	elif his.atomExists(" HD1"):
		H = his.getAtom(" HD1")
		A = his.getAtom(" NE2")
		B = his.getAtom(" CD2")
		C = his.getAtom(" CG ")
		name = " HE2"
	else:
		return

	if H == None or A == None or B == None or C == None:
		print "cannot find base atoms for switching tautomer"
		return

	crd = billder.dbuildAtom(A, B, C, 1.01, 126, 180)
	H.coord.x = crd[0]
	H.coord.y = crd[1]
	H.coord.z = crd[2]
	H.name = name



def closestApproachToResidue(atm=None, res=None):

	"""
	checks to see how close an atom comes to another residue
	"""

	mind = 1000.0
	if res.numAtoms() == 0:
		return mind

	for a in res.atom:
		d = atm.dist2(a)		

		if d < mind:
			mind = d
	
	return math.sqrt(mind)
		


def changeDihedral(A=None, B=None, C=None, D=None, tor=0.0):
	
	"""
	changes the position of an atom (A) by changing the torsion angle
	uses the previous distance and angle	
	(angles should be in degrees)
	"""

	if A == None or B == None or C == None or D == None:
		return	

	dist = A.distance(B)
	ang  = vector3d.angle3(A.coord,B.coord,C.coord)

	billder = Builder()
	crd = billder.dbuildAtom(B,C,D, dist, ang, tor)

	A.coord.x = crd[0]
	A.coord.y = crd[1]
	A.coord.z = crd[2]



def atomsAroundAtom(atm=None, mol=None, cutoff=6.0):
	
	"""
	returns a list of atoms within a cutoff of a given atom
	"""

	result = []
	if atm == None or mol == None:
		return result

	alist = mol.atomList()	
	c2 = cutoff*cutoff
	for a in alist:
		dist = a.dist2(atm)
		if dist < c2:
			result.append(a)	

	return result



def atomsAroundAtoms(atms=None, mol=None, atomList=None, cutoff=6.0):
	
	"""
	returns a list of atoms within a cutoff of a given set of atoms
	"""

	result = []
	if atms == None:
		return result

	if mol != None:
		atomList = mol.atomList()
	elif atomList == None:
		return result

	c2 = cutoff*cutoff
	for i in range(len(atms)):
		atm = atms[i]
		for a in atomList:
			dist = a.dist2(atm)
			if dist < c2:
				if not a in result:
					result.append(a)	

	return result



def residuesAroundAtom(atm=None, mol=None, cutoff=6.0):
	
	"""
	returns a list of residues that have an atom within a cutoff of a given atom
	"""

	result = []
	if atm == None or mol == None:
		return result

	rlist = mol.residueList()
	for r in rlist:
		dist = closestApproachToResidue(atm,r)
		if dist < cutoff:
			result.append(r)
	
	return result



def residuesAroundAtoms(atmlist=None, mol=None, cutoff=6.0):

	"""
	returns a list of residues that have an atom within a cutoff of given atoms
	"""
	
	result = []
	for atm in atmlist:
		inter = residuesAroundAtom(atm, mol, cutoff)
		for myres in inter:
			if not myres in result:
				result.append(myres)

	return result
		


def res_point_angle(residue=None, point=None):

	"""
	returns the angle of the CA-CB vector of a residue to a point in 3d space	
	"""

	if residue == None:
		print "residue_point_angle::no residue specified"
		return 0.0

	if point == None:
		print "residue_point_angle::no point sepecified"
		return 0.0

	CA = vector3d()
	CB = vector3d()
		
	foundCA = False
	foundCB = False

	if residue.name == "GLY":
		return 0.0

	for atm in residue.atom:
		if atm.name == " CA ":
			CA = atm.coord
			foundCA = True
		if atm.name == " CB ":
			CB = atm.coord
			foundCB = True

	if not foundCA or not foundCB:
		print "residue_point_angle::CA or CB not defined"
		return 0.0

	CA_CB = CB - CA
	CA_point = point - CA
	myang = CA_CB.angle(CA_point)

	return myang



def isResPointingToPoint(res=None, point=None, cutoff=90.0):

	"""
	checks to see if a residue is pointing to a point in space
	"""

	ang = res_point_angle(res, point)
	if abs(ang) < cutoff:
		return True
	
	return False



def isResPointingToRes(res1=None, res2=None, cutoff=90.0):
	
	"""
	checks to see if residue1 is pointing to any atom in residue2
	"""

	if res1 == None or res2 == None:
		print "residue == NONE"
		return False

	for atm in res2.atom:
		if isResPointingToPoint(res1,atm.coord,cutoff):
			return True

	return False



def reducePDBprecision(mol=None, precision=2):

	"""
	changes the pdb precision to 2 decimal places
	"""

	if mol == None:
		return

	change = 100.0
	if precision == 3:
		change = 1000.0
	elif precision == 2:
		change = 100.0
	elif precision == 1:
		change = 10.0
	elif precision == 0:
		change = 1.0


	for chain in mol.chain:
		for res in chain.residue:
			for atm in res.atom:
				mycoord = atm.coord
				mycoord *= change
				x = float(int(mycoord.x))/change
				y = float(int(mycoord.y))/change
				z = float(int(mycoord.z))/change
				atm.coord.x = x
				atm.coord.y = y
				atm.coord.z = z


def getRosettaElement(res=None,atm=None):

	"""
	gets the rosetta element
	"""

	alist = []
	if res != None:
		alist = res.atom
	elif atm != None:
		alist.append(atm)
	else:
		print "usage: getRosettaElement(res,atm)"
		sys.exit()

	for myatm in alist:
		if myatm.name in _rosetta_type.keys():
			myatm.element = _rosetta_type[myatm.name]
		else:
			print "unable to find rosetta element for: ",myatm.name

