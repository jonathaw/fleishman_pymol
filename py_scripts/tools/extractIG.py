#!/usr/bin/python

import string, sys
from optparse import OptionParser
from RotamerSet import *


def main():

	"""
reads rosetta-formatted energy values to create an Interaction graph
	"""

	parser = OptionParser()
	parser.add_option("-f", dest="file", help="file")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	nrotamers = 0
	none = 0
	ntwo = 0

	if not options.file or not options.outfile:
		parser.print_help()
		sys.exit()

	try:
		FILE = open(options.file)
	except:
		print "unable to open file"
		sys.exit()

	#ene = ["e1", "e2", "e3", "e4", "e5", "e6"]
	ene = ["e1", "e2", "e3"]

	try:
		OUTPUT = open(options.outfile, 'w')
	except:
		print "unable to open outfile"
		sys.exit()


	bNeigh = False;
	bInfo = False;
	rotamer = {}
	one_body = {}
	two_body = {}
	func = 0
	cfun = -1
	one = False
	two = False
	for line in FILE:
		line = string.rstrip(line)
		if line == "neighbor info":
			bNeigh = True
			OUTPUT.write("NEIGHBOR_INFO\n")
			print "reading neighbors"
			continue

		if line == "rotamer info":
			bInfo = True
			bNeigh = False
			OUTPUT.write("ROTAMER_INFO\n")
			print "reading rotamers"
			continue

		cols = line.split()
		if len(cols) < 2:
			continue

		if cols[0] == "function":
			ie  = ene[func]
			func += 1
			cfun += 1
			bInfo = False
			print "reading function",func
			continue

		if cols[1] == "body" and cols[0] == "2":
			two = True
			print "reading 2-body"
			continue

		if cols[1] == "body" and cols[0] == "1":
			one = True
			two = False
			print "reading 1-body"
			continue

		if bNeigh:
			OUTPUT.write(line + "\n")

		if bInfo:
			nrotamers += 1
			rotindex = int(cols[0])
			rotamer[rotindex] = {}
			one_body[rotindex] = {}
			rotamer[rotindex]["seqpos"] = cols[1]
			rotamer[rotindex]["aatype"] = cols[2]
			rotamer[rotindex]["rotnum"] = cols[3]
			rotamer[rotindex]["chi1"]   = cols[4]
			rotamer[rotindex]["chi2"]   = cols[5]
			rotamer[rotindex]["chi3"]   = cols[6]
			rotamer[rotindex]["chi4"]   = cols[7]
			two_body[rotindex] = {}
			OUTPUT.write(line + "\n")

		if two:
			ntwo += 1
			rotindex = int(cols[0])
			partner  = int(cols[1])

			if not two_body[rotindex].has_key(partner):
				two_body[rotindex][partner] = [0]*6
				#for i in range(6):
				#	two_body[rotindex][partner][ene[i]] = "0"

			two_body[rotindex][partner][cfun] = cols[2]

		if one:
			none += 1
			rotindex = int(cols[0])
			one_body[rotindex][ene[0]] = cols[1]
			#one_body[rotindex][ene[1]] = cols[2]
			#one_body[rotindex][ene[2]] = cols[3]
			#one_body[rotindex][ene[3]] = cols[4]
			#one_body[rotindex][ene[4]] = cols[5]
			#one_body[rotindex][ene[5]] = cols[6]
			one_body[rotindex][ene[1]] = cols[2]
			if len(cols) > 3:
				one_body[rotindex][ene[2]] = cols[3]

	FILE.close()

	print "number of rotamers =",nrotamers
	print "number of 1 body =",none
	print "number of 2 body =",ntwo

	# --- sort one body energies --- #		
	OUTPUT.write("ONE_BODY:\n")
	sl = rotamer.keys()
	sl.sort()
	for mykey in sl:
		line = ""
		line += str(mykey) + " " 

		#for i in range(6):
		for i in range(3):
			line += one_body[mykey][ene[i]] + " "

		OUTPUT.write(line + "\n")

	# --- sort two body energies --- #
	OUTPUT.write("TWO_BODY:\n")
	for mykey in sl:
		# ---   sort partners   --- #
		pl = two_body[mykey].keys()
		pl.sort()
		for plkey in pl:
			line = ""
			line += str(mykey) + " " + str(plkey) + " "
			#for i in range(6):
			for i in range(3):
				line += str(two_body[mykey][plkey][i]) + " "
			
			OUTPUT.write(line + "\n")
		

	OUTPUT.close()

	

if __name__ == "__main__":
	main()
