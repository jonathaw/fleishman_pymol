#!/usr/bin/python

"""

	vector3d.py

	class for storage and manipulation of 3d data

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import math


class vector3d:
	
	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x = x
		self.y = y
		self.z = z



	def __getitem__(self, item):

		"""
		returns the x,y, or z value
		"""

		if item == 0:
			return self.x
		if item == 1:
			return self.y
		if item == 2:
			return self.z

		return None



	def __setitem__(self,key,item):

		"""
		sets the x,y, or z value
		"""

		if key == 0:
			self.x = item
		if key == 1:
			self.y = item
		if key == 2:
			self.z = item


		
	def __neg__(self):

		"""
		returns the negative of the vector
		"""

		results = vector3d()
		results.x = -self.x
		results.y = -self.y
		results.z = -self.z
		return results



	def __add__(self, rhs):

		"""
		adds two vectors together
		"""

		results = vector3d()
		results.x = self.x + rhs.x	
		results.y = self.y + rhs.y	
		results.z = self.z + rhs.z	
		return results


	
	def __sub__(self, rhs):

		"""
		substracts one vector from another
		"""

		results = vector3d()
		results.x = self.x - rhs.x
		results.y = self.y - rhs.y
		results.z = self.z - rhs.z

		return results



	def __mul__(self, rhs):

		"""
		multiplies a vector by another vector or a scalar
		"""

		if isinstance(rhs, vector3d):
			return (self.x*rhs.x + self.y*rhs.y + self.z*rhs.z)
		elif isinstance(rhs, float) or isinstance(rhs,int):
			result = vector3d()
			result.x = self.x*rhs
			result.y = self.y*rhs
			result.z = self.z*rhs
			return result
		else:
			return None



	def __eq__(self, rhs):

		"""
		sets one vector equal to another or equal to a float
		"""

		if isinstance(rhs, vector3d):
			self.x = rhs.x
			self.y = rhs.y
			self.z = rhs.z
		elif isinstance(rhs, float) or isinstance(rhs,int):
			self.x = float(rhs)
			self.y = float(rhs)
			self.z = float(rhs)



	def __div__(self, rhs):

		"""
		divides a vector by a float
		"""

		result = vector3d()
		result.x = self.x/rhs
		result.y = self.y/rhs
		result.z = self.z/rhs
		return result



	def __repr__(self):

		"""
		prints out the vector
		"""

		return '%10.4f %10.4f %10.4f' % (self.x, self.y, self.z)



	def unit(self):

		"""
		returns the unit vector
		"""

		result = vector3d()
		length = self.length()
		if length > 0:
			result.x = self.x/length
			result.y = self.y/length
			result.z = self.z/length

		return result



	def length(self):

		"""
		returns the length of the vector
		"""

		return math.sqrt( (self.x*self.x) + \
				(self.y*self.y) + \
				(self.z*self.z) )



	def length2(self):

		"""
		returns the square of the length of the vector
		"""

		return (self.x*self.x) + (self.y*self.y) + (self.z*self.z)



	def distance(self, rhs=None):

		"""
		returns the distance between two vector positons
		"""

		return math.sqrt( ((self.x-rhs.x)*(self.x-rhs.x)) + \
				((self.y-rhs.y)*(self.y-rhs.y)) + \
				((self.z-rhs.z)*(self.z-rhs.z)) )



	def dist2(self, rhs=None):
		
		"""
		returns the square of the distance between two vectors
		"""

		dist2 = (self.x-rhs.x)**2 + \
			(self.y-rhs.y)**2 + \
			(self.z-rhs.z)**2

		return dist2	



	def cross(self, rhs=None):

		"""
		returns the cross product of two vectors
		"""

		result = vector3d()
		result.x = self.y*rhs.z - rhs.y*self.z
		result.y = self.z*rhs.x - rhs.z*self.x
		result.z = self.x*rhs.y - rhs.x*self.y
		return result



	def angle(self, rhs=None):

		"""
		returns the angle between two vectors (in degrees)
		"""

		ua = self.unit()
		ub = rhs.unit()

		dot = ua*ub
		myang = math.acos(dot)
		myang *= 57.2957795
		return myang



	def angle3(a,b,c):
		
		"""
		returns the angle between three points (in degrees)
		"""

		ab = a - b	
		cb = c - b
		return ab.angle(cb)



	def torsion(a, b, c, d):

		"""
		returns the torsion angle between 4 points
		"""

		ab = a - b
		cb = c - b
		cd = c - d

		p = ab.cross(cb)
		q = cb.cross(cd)

		p = p.unit()
		q = q.unit()

		ang = p.angle(q)

		pq = p.cross(q)
		s = cb*pq

		if s < 0:
			ang *= -1.0

		return ang



	def rotate(self, Mat):

		"""
		rotates a vector by a matrix
		"""

		tmp = [0.0, 0.0, 0.0]
		tmp2 = [self.x, self.y, self.z]
		for i in range(3):
			for j in range(3):
				tmp[i] += tmp2[j]*Mat[i][j]

		self.x = tmp[0]
		self.y = tmp[1]
		self.z = tmp[2]

