#!/usr/bin/python


"""

	SecondaryStructure.py

"""

__author__ = ['Andrew Wollacott amw215@u.washington.edu']
__version__ = 'Revision 0.1'

import string



class SecondaryStructure:

	def __init__(self):
		self.segments = []	
		self.sequence = ""

	

	def __getitem__(self, key):
		
		"""
		returns a segment of given index
		"""

		if key < 0 or key >= len(self.atom):
			return None

		return self.segments[key]



	def readSSfile(self, file=""):

		"""
		reads a file that specifies secondary structure segments
		"""

		if file == "":
			print "no file specified"
			return

		try:
			SSFILE = open(file, 'r')
		except:
			print "unable to open SS file"
			return

		seq = ""
		for line in SSFILE.readlines():
			line = string.strip(line)
			line = line.replace(" ", "")
			seq += line

		self.sequence = seq



	def newSegment(self):

		"""
		creates a new segment in the array
		"""

		newseg = SSelement()
		self.segments.append(newseg)
		return newseg


	def numSegments(self):

		"""
		returns the number of segments in the class
		"""

		return len(self.segments)



	def numHelices(self):

		"""
		returns the number of helices in the class
		"""

		nH = 0
		for seg in self.segments:
			if seg.type1 == "H":
				nH += 1

		return nH



	def numSheets(self):

		"""
		returns the number of sheets in the class
		"""

		nS = 0
		for seg in self.segments:
			if seg.type1 == "E":
				nS += 1

		return nS



	def numLoops(self):

		"""
		returns the number of loopsin the class
		"""

		nL = 0
		for seg in self.segments:
			if seg.type1 == "L":
				nL += 1

		return nL



	def parse(self):

		"""
		parses a secondary structure sequence
		"""

		if self.sequence == "":
			return

		ns = len(self.sequence)
		
		ss = self.sequence
		for i in range(ns):
			if ss[i] != "H" and ss[i] != "E" and ss[i] != "L":
				ss = ss.replace(ss[i], "L")

		running = 0
		seg = 0
		for i in range(1,ns):
			ss1 = ss[i]
			ssp = ss[i-1]

			if ss1 == ssp:
				if not running:
					seg = self.newSegment()
					seg.begin = i
					seg.end   = ns
					seg.size  = seg.end - seg.begin + 1
					seg.type1 = ssp
					running = 1
			else:
				if running:
					seg.end = i
					seg.size = seg.end - seg.begin + 1
					running = 0
					


	def printSequence(self):

		"""
		prints the secondary structure sequence
		"""

		ss = self.formatSequence()
		print ss



	def formatSequence(self):

		"""
		formats the sequence for output
		"""

		ns = len(self.sequence)
		out = ""
		for i in range(1,ns+1):
			if i % 50 == 0:
				out += self.sequence[i-1] + "\n"
			elif i % 10 == 0:
				out += self.sequence[i-1] + " "	
			else:
				out += self.sequence[i-1]

		return out



	def printRegions(self):

		"""
		print the segments in the molecule
		"""

		for seg in self.segments:
			print seg
		


class SSelement:

	"""
	class used to hold a contiguous secondary structural element
	"""
	
	def __init__(self):
		self.begin = 0
		self.end   = 0
		self.size  = 0
		self.type1 = ""
		self.type  = ""
		self.segment = " "


	def __repr__(self):
		return self.type1 + " " + str(self.segment) + " "  + str(self.begin) + "-" + str(self.end)

