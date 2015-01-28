#!/usr/bin/python


from optparse import OptionParser
from Gnuplot import *
import os, string, sys



def main():
	
	parser = OptionParser()
	parser.add_option("-f", dest="plotfile", help="plotfile")
	(options, args) = parser.parse_args()

	if not options.plotfile:
		parser.print_help()
		sys.exit()

	
	gnuplot = Gnuplot()
	gnuplot.term = "ps"
	gnuplot.title = "test"
	gnuplot.axis["xlabel"] = "RMSD"
	gnuplot.axis["ylabel"] = "SCORE"
	gnuplot.add_data(options.plotfile, "1a620")
	gnuplot.add_data("1avaB.plot", "1avaB")
	gnuplot.data[1].color=1
	gnuplot.size = 1.0
	gnuplot.run()


	
if __name__ == "__main__":
	main()

