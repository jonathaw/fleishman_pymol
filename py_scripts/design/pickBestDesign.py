#!/usr/bin/python

import string, sys, re, commands
from optparse import OptionParser
from file_routines import *

def main():

	"""
ranks the best designs of unique sequence using the formula:
E = bk_tot + lambda*lig_score + 
	"""

	parser = OptionParser()
	parser.add_option("-l", dest="file_list", help="file list")
	parser.add_option("-s", dest="scale", help="lig score scaling (5.0)", default = 5.0)
	parser.add_option("-k", dest="keep", help="number to keep", default = 1)
	parser.add_option("-i", dest="inverse", help="inverse", action="store_true")
	parser.set_description(main.__doc__)
	(options,args) = parser.parse_args()

	if not options.file_list:
		parser.print_help()
		sys.exit()

	scaling = float(options.scale)

	try:
		LIST = open(options.file_list)
	except:
		print "unable to open file list"
		sys.exit()

	list = []
	for i in LIST.readlines():
		i = string.rstrip(i)
		list.append(i)

	# get the bk_tot
	bk_tot = []
	for file in list:
		tmp = commands.getoutput("grep bk_tot " + file)
		cols = tmp.split()
		bk_tot.append(float(cols[1]))

	# get the sequence
	tmp = commands.getoutput("Sequence.py -P list")
	sequence = tmp.split("\n")

	# get the ligand score
	ligscore = []
	tmp = commands.getoutput("ligandScore.py -P list")
	tmp2 = tmp.split("\n")
	for i in tmp2:
		cols = i.split()
		ligscore.append(float(cols[4]))

	if len(ligscore) != len(sequence):
		print "ligand score and sequence arrays differ in length"
		sys.exit()

	tot_score = []
	for i in range(len(ligscore)):
		tot_score.append(bk_tot[i] + scaling*ligscore[i])

	uniq_seq = {}
	for i in range(len(list)):
		file = list[i]
		seq = sequence[i]
		if not seq in uniq_seq.keys():
			uniq_seq[seq] = {}

		uniq_seq[seq][file] = tot_score[i]

	keep = []
	nkeep = int(options.keep)
	for key in uniq_seq:
		srt= uniq_seq[key].items()
		srt.sort(lambda x,y:cmp(x[1],y[1]))
		ni = 0
		for i in srt:
			#print i[0],i[1]
			if (ni < nkeep):
				keep.append(i[0])
			ni += 1

	if options.inverse:
		for file in list:
			if not (file in keep):
				print file
	else:
		for file in keep:
			print file


	
	
		




if __name__ == "__main__":
	main()
