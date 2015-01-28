#!/usr/bin/python

import string, sys, os


class ProteinLibrary:

	def __init__(self):
		self.residue = {}



	def readLibrary(self, file=""):
		if file == "":
			return

		try:
			LIB = open(file)
		except:
			print "unable to open library",file
			sys.exit()

		cols = []
		intm = []
		atms = []
		for line in LIB.readlines():
			line = string.strip(line)
			cols = string.split(line, " ", 1)

			intm = string.split(cols[1], "'")
			atms = string.split(intm[1], ";")

			resn = cols[0]
			self.residue[resn] = []
			for atom in atms:
				self.residue[resn].append(atom)

			
