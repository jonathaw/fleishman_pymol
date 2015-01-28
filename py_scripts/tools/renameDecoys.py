#!/usr/bin/python

from optparse import OptionParser
import os, sys, string



def main():

	"""
renames a list of pdbfiles in ascending order
	"""
	
	parser = OptionParser()
	parser.add_option("-l", dest="list", help="list")
	parser.add_option("-b", dest="base", help="base")
	parser.add_option("-n", dest="number", help="base")
	parser.set_description(main.__doc__)
	(options, args) = parser.parse_args()


	if not options.list or not options.base or not options.number:
		parser.print_help()
		sys.exit()

	try:
		LIST = open(options.list)
	except:
		print "unable to open list"
		sys.exit()

	files = []
	renamed = []
	for line in LIST.readlines():
		line = string.strip(line)
		files.append(line)
			
	nfiles = len(files)	
	number = int(options.number)
	num = ""
	for i in range(nfiles):
		n = i + number
		if n < 10:
			num = "000" + str(n)
		if n >= 10 and n < 100:
			num = "00" + str(n)
		if n >= 100 and n < 1000:
			num = "0" + str(n)
		if n >= 1000 and n < 10000:
			num = str(n)
		if n >= 10000:
			print "more than 10,000 decoys"
			sys.exit()

		file = options.base + "_" + num + ".pdb"
		renamed.append(file)

	for i in range(nfiles-1,-1,-1):
		rename = "mv " + files[i] + " " + renamed[i]
		os.system(rename)


if __name__ == "__main__":
	main()
