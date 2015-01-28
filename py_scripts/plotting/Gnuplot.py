#!/usr/bin/python


"""

	Gnuplot.py

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import os, string


class Gnuplot:
	def __init__(self,file="gnplt"):
		self.outfile = "plot.ps"
		self.file    = file
		self.term    = "aqua"
		self.title   = ""
		self.size   = 1.0
		self.show_title = 1

		self.legend  = gnuplot_legend()

		self.axis = {}
		self.axis["xlabel"] = ""
		self.axis["ylabel"] = ""

		self.range = {}
		self.range["xmin"] = 0
		self.range["xmax"] = ""
		self.range["ymin"] = ""
		self.range["ymax"] = ""

		self.data = []


	def add_data(self,file,title=""):
		itsData = gnuplot_dataset()
		itsData.file = file
		itsData.title = title
		self.data.append(itsData)



	def write(self):
		try:
			PLOT = open(self.file, 'w')
		except:
			print "cannot open file"
			return 0

		if self.term == "ps":
			PLOT.write("set term postscript color enhanced\n")
			PLOT.write("set output '" + self.outfile + "'\n")
			PLOT.write("set encoding iso_8859_1\n")

		if self.show_title:
			PLOT.write("set title '" + self.title +  "'\n")

		self.legend.write(PLOT)

		PLOT.write("set size " + str(self.size) + "," + str(self.size) + "\n")
		PLOT.write("set xlabel '" + self.axis["xlabel"] + "'\n")
		PLOT.write("set ylabel '" + self.axis["ylabel"] + "'\n")
		PLOT.write("set tics out\n")
		PLOT.write("set xtics nomirror\n")
		PLOT.write("set ytics nomirror\n")

		
		PLOT.write("plot ")
		nfiles = len(self.data)
		for i in range(nfiles):
			data = self.data[i]
			PLOT.write("'" + data.file + "' using 2:3 title '" + data.title + "'") 
			PLOT.write(" ps " + str(data.point_size))
			PLOT.write(" pt " + str(data.point_type)) 
			PLOT.write(" lt " + str(data.color))

			if i == (nfiles-1):
				PLOT.write("\n")
			else:
				PLOT.write(",\\\n")


			

		PLOT.close()
				
			

	def run(self):
		self.write()
		os.system("gnuplot < " + self.file)


class gnuplot_dataset:
	def __init__(self, title=""):
		self.title = title
		self.point_size = 1.0
		self.point_type = 7
		self.color      = 3
		self.file       = ""



class gnuplot_legend:
	def __init__(self):
		self.show = 1
		self.box  = 1
		self.position = "right bottom"


	def write(self, stream=None):
		if self.show:
			stream.write("set key on\n")
			if self.box:
				stream.write("set key box\n")
			stream.write("set key " + self.position + "\n")
		else:
			stream.write("set key off\n")

