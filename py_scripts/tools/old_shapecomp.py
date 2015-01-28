#!/usr/bin/python

import os, sys, string
from optparse import OptionParser
from DotLib import *
from Enzyme import *
from MolSurface import *
from mol_routines import *
from file_routines import *

def main():

	"""
checks for shape complementarity for the enzyme
	"""

	parser = OptionParser()
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
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


	# --- read in dot information --- #
	home = os.environ["pyScriptsDir"]
	dotfile = home + "/data/sa64.dat"
	dotlib = DotLib()
	dotlib.read(dotfile)

	protein = Enzyme()
	for pdbfile in pdbfiles:
		protein.readPDB(pdbfile)
		ligAtoms = protein.ligand.atom

		atomlist = []
		for a in ligAtoms:
			if a.radius == 0:
				continue
			atomlist.append(a)

		# --- get nearby atoms --- #
		prot = protein.protein
		nearbyatoms = atomsAroundAtoms(atms=atomlist, atomList=prot.atomList(), cutoff=7.0)


		ligand_molsurf = MolSurface(dotlib)
		ligand_molsurf.setAtoms(atomlist)
		ligand_molsurf.extractSurface()
		mypnts = ligand_molsurf.identifyExposed(atomlist=nearbyatoms)
		ligand_molsurf.removePoints(mypnts,buffer=1.5)
		ligand_molsurf.extractNormals()
		#ligand_molsurf.printSurfacePoints(" O  ")
		#ligand_molsurf.printNormals(" N  ")
		#return

		active_molsurf = MolSurface(dotlib)
		active_molsurf.setAtoms(nearbyatoms)
		active_molsurf.extractSurface()
		active_molsurf.restrictToNearby(atomlist=atomlist,buffer=2.8)
		mypnts = active_molsurf.identifyExposed(atomlist)
		active_molsurf.removePoints(mypnts,buffer=1.5)
		active_molsurf.extractNormals()
		#active_molsurf.printSurfacePoints(" N  ")
		#active_molsurf.printNormals(" O  ")
		#return

		# --- get shape complementarity --- #
		S_ab = []
		for ilig in range(ligand_molsurf.numPoints()):
			xa = ligand_molsurf.points[ilig]
			# must be shielded from solvent
			iactive = active_molsurf.closestPoint(xa)
			if iactive == -1:
				continue

			xb = active_molsurf.points[iactive]
			na = ligand_molsurf.normals[ilig]
			tb = active_molsurf.normals[iactive]
			nb = vector3d(-tb.x,-tb.y,-tb.z)

			dist2 = -0.5*xa.dist2(xb)
			dotp  = na*nb
			ans   = dotp * math.exp(dist2)
			S_ab.append(float(ans))

		S_ba = []
		for iAct in range(active_molsurf.numPoints()):
			xb = active_molsurf.points[iAct]
			# must be shielded from solvent
			ilig = ligand_molsurf.closestPoint(xb)
			if ilig == -1:
				continue

			xb = active_molsurf.points[iAct]
			nb = active_molsurf.normals[iAct]

			xa = ligand_molsurf.points[ilig]
			ta = ligand_molsurf.normals[ilig]
			na = vector3d(-ta.x,-ta.y,-ta.z)

			dist2 = -0.5*xa.dist2(xb)
			dotp  = math.fabs(na*nb)
			ans   = dotp * math.exp(dist2)
			S_ba.append(float(ans))

		S_ab.sort()
		S_ba.sort()

		med_index_ab = len(S_ab)/2
		med_index_ba = len(S_ba)/2

		print med_index_ab
		print "Sab = ",S_ab[med_index_ab]

		SC = 0.5*(S_ab[med_index_ab] + S_ba[med_index_ba])
		print "SC = ",SC

		
		protein.clear()



if __name__ == "__main__":
	main()
