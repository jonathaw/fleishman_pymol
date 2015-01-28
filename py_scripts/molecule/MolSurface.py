

"""

	MolSurface.py

	a class storing molecular surfaces

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from vector3d import *
from Molecule import *


class MolSurface:


	def __init__(self, dotlib = None):
		self.points = []
		self.atoms = []
		self.center = []
		self.dotlib = dotlib
		self.normals = []
		self.closelist = []


	def numPoints(self):

		return len(self.points)


	def setAtoms(self,atomlist=None):

		"""
		sets all the atomic coordinates
		"""

		if len(atomlist) == 0:
			print "no atoms in list"
			return

		for a in atomlist:
			self.atoms.append(a)


	def printSurfacePoints(self, atmname=" C  "):

		myatom = Atom()
		myatom.name = atmname
		for point in self.points:
			myatom.coord = point
			print myatom

	
	def printNormals(self, atmname=" O  "):

		myatom = Atom()
		myatom.name = atmname
		npnts = len(self.points)
		for i in range(npnts):
			myatom.coord = self.normals[i]+self.points[i]
			print myatom
			


	def extractSurface(self, buffer=0.0):

		num_atoms = len(self.atoms)
		working_point = vector3d()
		print_atom = Atom()
		self.closelist = []
		for i in range(num_atoms):
			#tmp_close = []
			self.closelist.append([])
			self.closelist[i].append(i)
			for j in range(num_atoms):
				if i == j:
					continue

				iatom = self.atoms[i]
				jatom = self.atoms[j]

				rad_sum = iatom.radius + jatom.radius + buffer

				dist_ij = iatom.distance(jatom)

				if dist_ij <= rad_sum+2*buffer:
					self.closelist[i].append(j)


			mysize = buffer + iatom.radius
			for point in self.dotlib.points:
				buried = False

				working_point.x = mysize*point.x + iatom.coord.x
				working_point.y = mysize*point.y + iatom.coord.y
				working_point.z = mysize*point.z + iatom.coord.z
				for j in self.closelist[i]:
					if j == i:
						continue
					jatom = self.atoms[j]
					if working_point.distance(jatom.coord) <= (jatom.radius + buffer):
						buried = True
						break

				if buried:
					continue

				keep_point = vector3d(working_point.x,working_point.y,working_point.z)
				self.points.append(keep_point)
				self.center.append(i)
					

	def extractNormals(self,buffer=0.0):

		if len(self.points) == 0:
			print "must extract surface first"
			return

		npoints = len(self.points)
		self.normals = []
		for i in range(npoints):
			closest = []
			close_dist = []
			ipoint = self.points[i]
			icenter = self.center[i]
			for j in range(npoints):
				jcenter = self.center[j]
				if jcenter in self.closelist[icenter]:
					pass
				else:
					continue
					#pass

				if i == j:
					continue


				jpoint = self.points[j]
				dist = ipoint.dist2(jpoint)

				if dist < 0.50:
					#closest.append(jpoint)
					closest.append(j)
					close_dist.append(dist)

			# only choose the 3 closest
			tt = []
			if len(closest) > 4:
				close_dist.sort()
				min_dist = close_dist[4]

				for mm in closest:
					tt.append(mm)

				closest = []
				for mm in tt:
					if ipoint.distance(self.points[mm]) < min_dist:
						closest.append(mm)

			cen_vec = ipoint - self.atoms[self.center[i]].coord
			nclose = len(closest)
			normal_sum = vector3d(cen_vec.x,cen_vec.y,cen_vec.z)
			nclose = 0  # can erase!

			for j1 in range(nclose):
				for j2 in range(nclose):
					if j1 == j2:
						continue

					vector_ij1 = ipoint - self.points[closest[j1]]
					vector_ij2 = ipoint - self.points[closest[j2]]
					tmp_norm = vector_ij1.cross(vector_ij2)

					# make sure it points away from its atom base
					ang = tmp_norm.angle(cen_vec)
					if ang > 90.0:
						tmp_norm = -tmp_norm

					normal_sum += tmp_norm
			#	jvec = self.points[closest[j1]] - self.atoms[self.center[closest[j1]]].coord
			#	normal_sum += jvec

			nu = normal_sum.unit()
			self.normals.append(nu)


	def closestPoint(self, pnt, mindist=2.8):

		min_pnt = -1
		npnts = len(self.points)
		for ipnt in range(npnts):
			dist = pnt.dist2(self.points[ipnt])
			if dist < mindist:
				mindist = dist
				min_pnt = ipnt

		return min_pnt
			


	def fluffPoints(self, buffer):

		"""
		moves points out my a certain amount
		"""

		npnts = len(self.points)
		for ipnt in range(npnts):
			icen = self.center[ipnt]
			cen_crd = self.atoms[icen].coord
			vec = self.points[ipnt] - cen_crd
			vec *= buffer
			self.points[ipnt] += vec


	def identifyExposed(self,atomlist=None,buffer=2.8):

		exposed = []	
		for point in self.points:
			buried = False
			for atm in atomlist:
				if point.distance(atm.coord) < (atm.radius+buffer):
					buried = True	
					break

			if buried == False:
				exposed.append(point)

		return exposed


	def removePoints(self, pntlist=None, buffer=1.5):

		nkeep = 0
		cp_points = []
		cp_center = []
		npnts = len(self.points)
		for i in range(npnts):
			point = self.points[i]
			buried = False
			for opnt in pntlist:
				if point.distance(opnt) < buffer:
					buried = True	
					break

			if buried == False:
				nkeep += 1
				cp_points.append(point)
				cp_center.append(self.center[i])

		self.points = []
		self.center = []
		for i in range(nkeep):
			self.points.append(cp_points[i])
			self.center.append(cp_center[i])

		


	def removeExposed(self, atomlist=None, buffer=1.4):

		nkeep = 0
		cp_points = []
		cp_center = []
		npnts = len(self.points)
		for i in range(npnts):
			point = self.points[i]
			buried = False
			for atm in atomlist:
				if point.distance(atm.coord) < (atm.radius+buffer):
					buried = True	
					break

			if buried == True:
				nkeep += 1
				cp_points.append(point)
				cp_center.append(self.center[i])

		self.points = []
		self.center = []
		for i in range(nkeep):
			self.points.append(cp_points[i])
			self.center.append(cp_center[i])


	def restrictToNearby(self, atomlist=None, buffer=2.8):

		npnts = len(self.points)
		cp_points = []
		cp_center = []
		nkeep = 0
		for ipnt in range(npnts):
			point = self.points[ipnt]
			buried = False
			for atm in atomlist:
				if point.distance(atm.coord) <= (atm.radius+buffer):
					buried = True	
					break

			if buried == True:
				cp_points.append(point)
				cp_center.append(self.center[ipnt])
				nkeep += 1

		self.points = []
		self.center = []

		for i in range(nkeep):
			self.points.append(cp_points[i])
			self.center.append(cp_center[i])

