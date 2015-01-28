#!/usr/bin/python

import string, sys
from optparse import OptionParser
from Molecule import *
from mol_routines import *
from file_routines import *


def main():

	"""
A generalized transformation tool.  The -T option specifies the type of transformation to perform
and are of the following types:
translate (t=x,y,z);
rotate (r=x,y,z,angle) (rotates about the center of mass);
Rotate (R=x,y,z,angle) (rotates but NOT using the center of mass);
	"""

	parser = OptionParser()
	parser.add_option("-p", dest="pdbfile", help="pdbfile")
	parser.add_option("-P", dest="pdblist", help="pdblist")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-O", dest="outlist", help="outlist")
	parser.add_option("-r", dest="replace", help="replace", action="store_true")
	parser.add_option("-T", dest="transform", help="transformations (semicolon delimited)")
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

	if not options.transform:
		parser.print_help()
		sys.exit()


	mol = Molecule()
	for i in range(len(pdbfiles)):
		mol.readPDB(pdbfiles[i])

		tlist = options.transform.split(";")

		myvec = vector3d()
		for op in tlist:
			cols = op.split("=")

			# translations
			if cols[0] == "t":
				cc = cols[1].split(",")
				if len(cc) != 3:
					print "translation must specify x,y,z movement"
					sys.exit()

				myvec.x = float(cc[0])
				myvec.y = float(cc[1])
				myvec.z = float(cc[2])
				mol.translate(myvec)

			# rotations
			elif cols[0] == "r" or cols[0] == "R":
				cc = cols[1].split(",")
				if len(cc) != 4:
					print "rotation must specify x,y,z vector and angle"
					sys.exit()

				myvec.x = float(cc[0])
				myvec.y = float(cc[1])
				myvec.z = float(cc[2])
				myang   = float(cc[3])

				if cols[0] == "r":
					com = mol.com()
					mol.translate(-com)

				rotateArbitraryAxis(mol, myvec, myang)

				if cols[0] == "r":
					mol.translate(com)

			else:
				print "unrecognized transformation"
				sys.exit()

		mol.writePDB(outfiles[i],resRenumber=False,atomRenumber=False)



if __name__ == "__main__":
	main()

