#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from mol_routines import *
from file_routines import *


def main():

	"""
	rotates a molecule about a major cartesian axis or about an arbitrary axis
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-v", dest="vector",  help="vector")
	parser.add_option("-x", dest="axis", help="axis")
	parser.add_option("-a", dest="angle", help="angle in degrees")
	parser.add_option("-c", dest="com", help="no rotation about center of mass")
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
	elif options.replace:
		for file in pdbfiles:
			outfiles.append(file)
	else:
		parser.print_help()
		sys.exit()


	myang = 0.0
	if options.angle:
		myang = float(options.angle)
	else:
		print "no angle specified"
		sys.exit()


	mol = Molecule()
	for i in range(len(pdbfiles)):
		mol.readPDB(pdbfiles[i])

		if not options.com:
			com = mol.com()
			mol.translate(-com)

		if options.axis:
			rotateAboutAxis(mol, options.axis, myang)
		elif options.vector:
			tmp = options.vector.split(",")
			if len(tmp) != 3:
				print "vector must specifiy three directions"
				sys.exit()

			myvec = vector3d()
			myvec.x = float(tmp[0])
			myvec.y = float(tmp[1])
			myvec.z = float(tmp[2])

			rotateArbitraryAxis(mol, myvec, myang)

		if not options.com:
			mol.translate(com)

		mol.writePDB(outfiles[i], resRenumber=False, atomRenumber=False)



if __name__ == "__main__":
	main()

