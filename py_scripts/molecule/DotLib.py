#!/usr/bin/python


"""

	DotLib.py

	a class storing information on atom masks

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from vector3d import *


class DotLib:


	def __init__(self):
		self.points = []


	def read(self,file=""):

		"""
		reads in the dot library
		"""

		try:
			DL = open(file)
		except:
			print "unable to open dot file:",file
			return

		lines = DL.readlines()
		for line in lines:
			cols = line.split()
			a = float(cols[0])
			b = float(cols[1])

			dp = vector3d()
			dp[0] = math.sin(a)*math.cos(b)
			dp[1] = math.sin(a)*math.sin(b)
			dp[2] = math.cos(a)

			self.points.append(dp)


	def numDots(self):
		
		"""
		returns the number of dots in a file
		"""
	
		return len(self.points)


