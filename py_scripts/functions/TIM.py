#!/usr/bin/python


import os, sys, string
from optparse import OptionParser
from SecondaryStructure import *


class TIM:

	"""
	storage class for the representation of TIM structures
	"""
	
	def __init__(self):
		self.SLH = []
		self.ss  = SecondaryStructure()



	def numSegments(self):

		"""
		returns the number of segments in a TIM object
		"""

		return len(self.SLH)



	def isInSegment(self, resi=-1):

		"""
		reports whether a residue is in a given segment
		"""

		if resi == -1:
			return 0

		for seg in self.SLH:
			segbeg = seg["sheet"].begin
			segend = seg["helix"].end

			if resi >= segbeg and resi <= segend:
				return 1


	def correspondingSegment(self, resi=-1):

		"""
		returns the segment that a residue is in
		"""

		resi = int(resi)

		nseg = 0
		for seg in self.SLH:
			nseg += 1
			segbeg = seg["sheet"].begin
			segend = seg["helix"].end

			if resi >= segbeg and resi <= segend:
				if resi >= seg["sheet"].begin and resi <= seg["sheet"].end:
					seg["sheet"].segment = nseg
					return seg["sheet"]

				if resi >= seg["loop"].begin and resi <= seg["loop"].end:
					seg["loop"].segment = nseg
					return seg["loop"]

				if resi >= seg["helix"].begin and resi <= seg["helix"].end:
					seg["helix"].segment = nseg
					return seg["helix"]

		return None


	
	def sort(self):

		"""
		sorts the TIM segments in numerical order
		"""

		tmp = []
		n = len(self.SLH)
			
		taken = {}
		for i in range(n):
			taken[i] = 0

		for i in range(n):
			minBeg = 88888
			for j in range(n):
				if taken[j]:
					continue

				jBeg = self.SLH[j]["sheet"].begin
				if jBeg < minBeg:
					minBeg = jBeg
					minIndex = j

			taken[minIndex] = 1
			tmp.append(self.SLH[minIndex])

		self.SLH = tmp


	def formatSegments(self):
		
		"""
		formats the segments for output
		"""

		self.sort()

		start = self.SLH[0]["sheet"].begin
		pos = 1
		ss = ""
		for seg in self.SLH:
			start = int(seg["sheet"].begin)
			end   = int(seg["helix"].end)

			space = start - pos
			ss += " " * space

			ss += "E" * int(seg["sheet"].size)
			ss += "L" * int(seg["loop"].size)
			ss += "H" * int(seg["helix"].size)

			pos = end + 1
			
		ns = len(ss)
		out = ""
		for i in range(1,ns+1):
			if i % 50 == 0:
				out += ss[i-1] + "\n"
			elif i % 10 == 0:
				out += ss[i-1] + " "
			else:
				out += ss[i-1]

		return out


	def newSLH(self):
		
		"""
		creates a new sheet-loop-helix motif
		"""

		myslh = {}
		self.SLH.append(myslh)

		myslh["helix"] = self.ss.newSegment()
		myslh["sheet"] = self.ss.newSegment()
		myslh["loop"] = self.ss.newSegment()

		return myslh


	def removeSLH(self, index=-1):

		"""
		removes a sheet-loop-helix motif of given index
		"""

		if index < 0:
			return

		self.SLH.pop(index)
	

	def setSequence(self, sequence):

		"""
		sets the secondary structural sequence for the TIM
		"""

		ss = SecondaryStructure()
		ss.sequence = sequence
		ss.parse()
		ns = ss.numSegments()

		for i in range(1,ns-1):
			if ss.segments[i].type1 == "L":	
				if ss.segments[i-1].type1 == "E" and ss.segments[i+1].type1 == "H":
					inter = self.newSLH()
					inter["helix"] = ss.segments[i+1]
					inter["sheet"] = ss.segments[i-1]
					inter["loop"]  = ss.segments[i]

	
	def readTIM(self, timfile):

		"""
		reads a TIM file in its own format
		"""

		try:
			TIMEH = open(timfile, 'r')
		except:
			print "unable to open timfile"

		cols = []
		inter = {}
		ss = SecondaryStructure
		for line in TIMEH.readlines():
			line = string.strip(line)

			if len(line) == 0:
				continue

			cols = line.split()
			if cols[0] == "SLH":
				inter = self.newSLH()

			if cols[0] == "SHEET":
				inter["sheet"].size  = int(cols[1])
				inter["sheet"].begin = int(cols[2])
				inter["sheet"].end   = int(cols[3])
				inter["sheet"].type1 = "sheet"

				
			if cols[0] == "LOOP":
				inter["loop"].size  = int(cols[1])
				inter["loop"].begin = int(cols[2])
				inter["loop"].end   = int(cols[3])
				inter["loop"].type1 = "loop"

			if cols[0] == "HELIX":
				inter["helix"].size  = int(cols[1])
				inter["helix"].begin = int(cols[2])
				inter["helix"].end   = int(cols[3])
				inter["helix"].type1 = "helix"

		TIMEH.close()



	def writeTIM(self, timfile):

		"""
		writes a TIM file in its own format
		"""

		try:
			TIM = open(timfile, 'w')
		except:
			print "unable to open timfile"

		n = 0
		for segment in self.SLH:
			loop  = segment["loop"]
			helix = segment["helix"]
			sheet = segment["sheet"]

			segbeg = sheet.begin
			segend = helix.end

			n += 1
			TIM.write("SLH " + str(n) + " " + str(segbeg) + " " + str(segend) +"\n")
			TIM.write("SHEET " + str(sheet.size) + " " + str(sheet.begin) + " " + str(sheet.end) + "\n")
			TIM.write("LOOP  " + str(loop.size) + " " + str(loop.begin) + " " + str(loop.end) + "\n")
			TIM.write("HELIX " + str(helix.size) + " " + str(helix.begin) + " " + str(helix.end) + "\n")
			TIM.write("\n")

		TIM.close()



	def writePymol(self, pyfile):
		
		"""
		writes a file in a format readable to pymol
		"""

		try:
			PYMOL = open(pyfile, 'w')
		except:
			print "unable to open pymol file"

		for seg in self.SLH:
			helix = seg["helix"]
			sheet = seg["sheet"]
			loop  = seg["loop"]

			PYMOL.write("color red, resi " + str(helix.begin) + "-" + str(helix.end) + "\n")
			PYMOL.write("color yellow, resi " + str(sheet.begin) + "-" + str(sheet.end) + "\n")
			PYMOL.write("color cyan, resi " + str(loop.begin) + "-" + str(loop.end) + "\n")
			
