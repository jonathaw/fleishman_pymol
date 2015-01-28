#!/usr/bin/python

import string, sys, re, commands
from optparse import OptionParser
from mol_routines import *
from file_routines import *
from match_routines import *
from Molecule import *
from Selection import *

def main():

	"""
clusters matches after minimization
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="list", help="list")
	parser.add_option("-o", dest="outfile", help="outfile")
	parser.add_option("-n", dest="number", help="number", default=5)
	parser.add_option("-v", dest="verbose", help="verbose", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.list or not options.outfile:
		parser.print_help()
		sys.exit()

	try:
		OUTFILE = open(options.outfile, 'w')
	except:
		print "unable to create outfile"
		sys.exit()


	match_list = files_from_list(options.list)
	rbmin_list = []
	for file in match_list:
		base = get_basefile(file)
		rbmin = base + "_rbmin.pdb"
		rbmin_list.append(rbmin)

	# --- make clusters based on location --- #
	clusters = {}
	protein = Molecule()
	for i in range(len(match_list)):
		file = match_list[i]
		cols = file.split("_")
		grid = cols[1]
		if not grid in clusters.keys():
			clusters[grid] = {}		

                protein.readPDB(file)
                cat = getCatalyticResidues(protein)

                seq = ""
                for c in cat:
                        seq += c.name + c.file_id.strip() + "_"	

		if not seq in clusters[grid].keys():
			clusters[grid][seq] = []

		clusters[grid][seq].append(rbmin_list[i])
		protein.clear()
	
	for grid in clusters.keys():
		if options.verbose:
			OUTFILE.write(grid+"\n")

		for seq in clusters[grid].keys():
			if options.verbose:
				OUTFILE.write("   seq: "+ seq+"\n")

			mycluster = clusters[grid][seq]
			scores = {}
			for file in mycluster:
				ene = commands.getoutput("grep lig_sum " + file)
				cols = ene.split()
				sum = float(cols[1])
				scores[file] = sum
		
			i = scores.items()
			i.sort(lambda x,y:cmp(x[1],y[1]))
			nbest = 0
			for bestfile in i:
				if options.verbose:
					OUTFILE.write("      "+bestfile[0] + " " + str(bestfile[1]) + "\n")
				else:
					output = bestfile[0].replace("_rbmin", "")
					OUTFILE.write(output+"\n")
				nbest += 1
				if nbest == int(options.number):
					break


		if options.verbose:
			OUTFILE.write("----------------\n")

	OUTFILE.close()

if __name__ == "__main__":
	main()
