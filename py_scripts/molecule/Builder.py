#!/usr/bin/python

"""

		Builder.py

		The builder class facilitates the building of atoms

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import math
from vector3d import *


class Builder:
	
	def __init__(self):
		self.name = ""

	

	def buildCoords(self, b, c, d, dist, ang, tor):

		"""
		function buildCoords: builds the coordinates of a new position based on the 
		positions of the previous three atoms and a length, angle, and torsion
		"""

		# buildCoords
		#
		#     B -- C
		#   /        \
		# A           D
		#

		p = b - c 
		q = d - c

		p = p.unit()
		q = q.unit()
		
		r = p.cross(q)
		r = r.unit()

		s = r.cross(p)
		s = s.unit()

		a = b -  p*dist*math.cos(ang) + r*dist*math.sin(ang)*math.sin(tor) + s*dist*math.sin(ang)*math.cos(tor)

		return a



	def buildAtom(self, atom2, atom3, atom4, dist, ang, tor):

		"""
		function buildAtom: builds and atom from the previous three atoms given a
		bond length, angle, and torsion
		uses radians
		"""

		b = vector3d(atom2.coord[0], atom2.coord[1], atom2.coord[2])
		c = vector3d(atom3.coord[0], atom3.coord[1], atom3.coord[2])
		d = vector3d(atom4.coord[0], atom4.coord[1], atom4.coord[2])

		a = self.buildCoords(b, c, d, dist, ang, tor)
		result = [a.x, a.y, a.z]
		return result


	def dbuildAtom(self, atom2, atom3, atom4, dist, ang, tor):

		"""
		function buildAtom: builds and atom from the previous three atoms given a
		bond length, angle, and torsion
		uses degrees
		"""

		ang = ang * 0.0174532925
		tor = tor * 0.0174532925

		return self.buildAtom(atom2, atom3, atom4, dist, ang, tor)

