#!/usr/bin/python


from Alias import *
from NMRspectrum import *
from optparse import OptionParser



def main():

	"""
	converts atom names in an NMR spectrum to standard atom names
	"""

	parser = OptionParser()
	parser.add_option("-s", dest="spectrum", help="spectrum")
	parser.add_option("-o", dest="outfile", help="outfile")
	(options, args) = parser.parse_args()

	alias = Alias()
	spec  = NMRspectrum()
	

if __name__ == "__main__":
	main()
