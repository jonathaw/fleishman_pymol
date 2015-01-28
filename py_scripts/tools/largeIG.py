#!/usr/bin/python

import string, sys
from optparse import OptionParser
from pdb_routines import *

def main():

	"""
reads large rosettta-formatted interaction graphs
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-c", dest="column", help="column")
	parser.add_option("-v", dest="value", help="value")
	parser.add_option("-t", dest="type", help="type")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	nrotamers = 0
	none = 0
	ntwo = 0

	if not options.file or not options.outfile:
		parser.print_help()
		sys.exit()

	if options.type:
		type1 = num_from_aa1(options.type[0])
		type2 = num_from_aa1(options.type[1])

	try:
		FILE = open(options.file)
	except:
		print "unable to open file"
		sys.exit()

	try:
		OUTPUT = open(options.outfile, 'w')
	except:
		print "unable to open outfile"
		sys.exit()

	bRead = False
	if options.value:
		fvalue = float(options.value)
	nline = 0
	keep = {}
	nkept = 0
	aatype = {}
	print "reading through first"
	bReadRot = False
	for line in FILE:
		cols = line.split()
		if cols[0] == "function":
			bReadRot = False
			if cols[1] == options.column:
				bRead = True
			else:
				bRead = False
			continue

		if cols[0] == "rotamer":
			bReadRot = True
			continue

		if bReadRot:
			aatype[cols[0]] = int(cols[2])
			

		if bRead:
			if cols[1] == "body":
				if cols[0] == "1":
					bRead=False
				continue

			if options.type:
				if aatype[cols[0]] == type1 and aatype[cols[1]] == type2:
					pass
				elif aatype[cols[0]] == type2 and aatype[cols[1]] == type1:
					pass
				else:
					key = cols[0] + "_" + cols[1]
					keep[key] = True
					nkept += 1
					continue

				if options.value:
					if float(cols[2]) < fvalue:
						key = cols[0] + "_" + cols[1]
						keep[key] = True
						nkept += 1
			else:		
				if float(cols[2]) < fvalue:
					key = cols[0] + "_" + cols[1]
					keep[key] = True
					nkept += 1

	FILE.close()
	print nkept,"kept"
	print "reading through second"
	FILE = open(options.file)

	bEverything = True
	bEnergy = False
	bType = False
	for line in FILE:
		cols = line.split()
		if cols[1] == "body" and cols[0] == "2":
			if options.type:
				bType = True
			if options.value:
				bEnergy = True

			bEverything = False
			OUTPUT.write(line)
			continue

		if cols[1] == "body" and cols[0] == "1":
			bEverything = True
			bEnergy = False
			bType = False
			OUTPUT.write(line)
			continue

		if bEverything:
			OUTPUT.write(line)


		if bType and not bEnergy:
			if cols[0] == "function":
				OUTPUT.write(line)
				continue

			if aatype[cols[0]] == type1 and aatype[cols[1]] == type2:
				pass
			elif aatype[cols[0]] == type2 and aatype[cols[1]] == type1:
				pass
			else:
				OUTPUT.write(line)

			

		if bEnergy:
			if cols[0] == "function":
				OUTPUT.write(line)
				continue

			mykey = cols[0] + "_" + cols[1]
			if keep.has_key(mykey):
				OUTPUT.write(line)



	FILE.close()
	OUTPUT.close()

if __name__ == "__main__":
	main()
