#!/usr/bin/python


"""

	Loop_collection.py

	stores a list of loop libraries

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import re,sys,string
from Loop_library import *



class Loop_collection:


	def __init__(self):
		self.loops = []


	def read(self, file):
		
		"""
		reads in a loop library file
		"""

		try:
			LOOP_LIB = open(file)
		except:
			print "error opening loop library",file
			sys.exit()

		re_loop = re.compile("LOOP")
		re_file = re.compile("FILE")
		loop = None
		bReadLoop = False
		for line in LOOP_LIB.readlines():
			line = string.rstrip(line)

			if re_loop.match(line):
				loop = self.newLoopLibrary()
				cols = line.split()
				loop.start_point = int(cols[1])
				loop.end_point   = int(cols[2])
				bReadLoop = True

			if re_file.match(line):
				if loop == None:
					continue

				print line
				cols = line.split()
				loop.read(cols[1])



	def newLoopLibrary(self):

		myloop = Loop_library()
		self.loops.append(myloop)

		return myloop


	def getLoopLibrary(self,resid):

		"""
		returns a loop library with a given resid
		"""

		for loop in self.loops:
			if loop.start_point <= resid and loop.end_point >= resid:
				return loop	

		return None


	def setNative(self, nat):

		for loop in self.loops:
			reslist = nat.chain[0].getResidues(loop.start_point, loop.end_point)
			loop.addLoop(reslist)

