#!/usr/bin/python


"""

	InteractionGraph.py

	The interaction graph handles a two-body energy table

"""

__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

from vector3d import *
from Rotamer import *
from pdb_routines import *
import string, sys

class InteractionGraph:



	def __init__(self):
		self.neighbors = {}
		self.nodes = []
		self.edges = []
		self.rotamers = []


	def renumberRotamers(self, startnum):

		"""
		renumbers rotamer indices
		and returns the index of the last rotamer
		"""

		irot = startnum
		mapping = {}
		for rot in self.rotamers:
			cindex = rot.index
			rot.index = irot
			mapping[cindex] = irot
			irot += 1

		for one_bod in self.nodes:
			cindex = one_bod.rotindex
			one_bod.rotindex = mapping[cindex]

		for two_bod in self.edges:
			cindex1 = two_bod.rotindex1
			cindex2 = two_bod.rotindex2
			two_bod.rotindex1 = mapping[cindex1]
			two_bod.rotindex2 = mapping[cindex2]

		return irot


	def combineIG(self, rhs):

		"""
		combines two Interaction graphs to form 1
		"""

		# renumber rotamers
		last_index = self.renumberRotamers(1)
		rhs.renumberRotamers(last_index)


		# copy neighbors
		for key in rhs.neighbors.keys():
			self.neighbors[key] = rhs.neighbors[key]

		# first clone rotamers
		for rot in rhs.rotamers:
			myrot = Rotamer()
			rot.clone(myrot)
			self.rotamers.append(myrot)

		# THESE SHOULD BE DEEP COPIES
		# CHANGE!!!!
		for node in rhs.nodes:
			self.nodes.append(node)

		for edge in rhs.edges:
			self.edges.append(edge)

		self.commonRotamers()
		self.clean()
			


	def read(self, file=""):

		"""
		function read: reads in the interaction graph (own format required)
		"""

		if file == "":
			print "usage: read(file)"
			return

		try:
			FILE = open(file)
		except:
			print "unable to open file:",file
			sys.exit()
			return
			
		bNeigh = False
		bRot = False
		bOne = False
		bTwo = False
		tmpType = {}
		for line in FILE:
			line = string.rstrip(line)
			if line == "NEIGHBOR_INFO":
				bNeigh = True
				continue

			if line == "ROTAMER_INFO":
				bRot = True
				bNeigh = False
				continue

			if line == "ONE_BODY:":
				#print "setting up one body terms"
				bOne = True
				bRot = False
				continue

			if line == "TWO_BODY:":
				#print "setting up two body terms"
				bOne = False
				bTwo = True
				continue

			cols = line.split()

			if bNeigh:
				self.neighbors[int(cols[0])] = int(cols[1])

			if bRot:
				rot = Rotamer()
				rot.index  = int(cols[0])
				rot.seqpos = int(cols[1])
				rot.aatype = int(cols[2])
				rot.state  = int(cols[3])

				rot.chi1   = float(cols[4])
				rot.chi2   = float(cols[5])
				rot.chi3   = float(cols[6])
				rot.chi4   = float(cols[7])
				
				self.rotamers.append(rot)
				tmpType[rot.index] = rot.aatype

			if bOne:
				onebody = one_body_interaction()
				onebody.rotindex = int(cols[0])
				onebody.set_energy("Erep", float(cols[1]))
				#onebody.set_energy("Eatr", float(cols[2]))
				#onebody.set_energy("Esol", float(cols[3]))
				#onebody.set_energy("Ehbb", float(cols[4]))
				#onebody.set_energy("Ehbbsc", float(cols[5]))
				#onebody.set_energy("Ehsc", float(cols[6]))
				onebody.set_energy("Ehsc", float(cols[2]))
				if len(cols) > 3:
					onebody.set_energy("Ehbbsc", float(cols[3]))
				else:
					onebody.set_energy("Ehbbsc", 0.0)
				self.nodes.append(onebody)

			if bTwo:
				twobody = two_body_interaction()
				twobody.rotindex1 = int(cols[0])
				twobody.rotindex2 = int(cols[1])
				twobody.type1 = tmpType[twobody.rotindex1]
				twobody.type2 = tmpType[twobody.rotindex2]
				twobody.set_energy("Erep", float(cols[2]))
				#twobody.set_energy("Eatr", float(cols[3]))
				#twobody.set_energy("Esol", float(cols[4]))
				#twobody.set_energy("Ehbb", float(cols[5]))
				#twobody.set_energy("Ehbbsc", float(cols[6]))
				#twobody.set_energy("Ehsc", float(cols[7]))
				twobody.set_energy("Ehsc", float(cols[3]))
				if len(cols) > 4:
					twobody.set_energy("Ehbbsc", float(cols[4]))
				else:
					twobody.set_energy("Ehbbsc", 0.0)
				self.edges.append(twobody)


		FILE.close()
		#print "done"



	def write(self, file):

		"""
		function write: the interaction graph writes its contents in its own format
		"""

		if file == "":
			print "usage: write(file)"
			return

		try:
			OUTPUT = open(file, 'w')
		except:
			print "unable to open file:",file
			sys.exit()

		# --- write out neighbors --- #
		OUTPUT.write("NEIGHBOR_INFO\n")
		sortkey = self.neighbors.keys()
		sortkey.sort()
		for key in sortkey:
			OUTPUT.write(str(key) + " " + str(self.neighbors[key]) + "\n")

		# --- write out rotamers --- #
		OUTPUT.write("ROTAMER_INFO\n")
		for rot in self.rotamers:
			OUTPUT.write(
				str(rot.index) + " " + 
				str(rot.seqpos) + " " + 
				str(rot.aatype) + " " + 
				str(rot.state) + " " + 

				str(rot.chi1) + " " + 
				str(rot.chi2) + " " + 
				str(rot.chi3) + " " + 
				str(rot.chi4) + "\n" )

		# --- write out one-body terms --- #
		OUTPUT.write("ONE_BODY:\n")
		for node in self.nodes:
			OUTPUT.write(
				str(node.rotindex) + " " + 
				str(node.energies["Erep"]) + " " + 
				#str(node.energies["Eatr"]) + " " + 
				#str(node.energies["Esol"]) + " " + 
				#str(node.energies["Ehbb"]) + " " +
				#str(node.energies["Ehbbsc"]) + " " +
				str(node.energies["Ehsc"]) + " " +
				str(node.energies["Ehbbsc"]) + "\n")


		OUTPUT.write("TWO_BODY:\n")
		for edge in self.edges:
			OUTPUT.write(
				str(edge.rotindex1) + " " + 
				str(edge.rotindex2) + " " + 
				str(edge.energies["Erep"]) + " " + 
				#str(edge.energies["Eatr"]) + " " + 
				#str(edge.energies["Esol"]) + " " + 
				#str(edge.energies["Ehbb"]) + " " +
				#str(edge.energies["Ehbbsc"]) + " " +
				str(edge.energies["Ehsc"]) + " " +
				str(edge.energies["Ehbbsc"]) + "\n")

		OUTPUT.close()



	def keepRotamerList(self, aatype, list):

		"""
		function keepRotamerList: keeps the rotamers of given amino acid type from a list of 
		rotamer indices
		"""

		count = 0
		failed = {}
		for rot in self.rotamers:
			if rot.aatype == aatype:
				ind_found = False
				for index in list:
					if rot.index == index:
						ind_found = True
						break
					
				if not ind_found:
					failed[rot.index] = True
					count += 1

		print count, " to be removed"
		status = 0
		for index in failed.keys():
			status += 1
			if (status == 100):
				print ".",
				status = 0

			self.removeRotamer(index)

		self.clean()



	def keepPositions(self, aatype, list):

		"""
		function keepPositions: keeps the rotamers of given amino acid type that have
		a resiude index in the list
		"""

		failed = {}
		for rot in self.rotamers:
			rot_found = True
			if rot.aatype == aatype:
				rot_found = False
				if rot.seqpos in list:
					rot_found = True

			if not rot_found:
				failed[rot.index] = True
					
		print "removing",len(failed),"rotamers"
		for index in failed.keys():
			self.removeRotamer(index)

		self.clean()
				
			
			
	def removeRotamer(self, rotindex):

		"""
		function removeRotamer: removes a rotamer of given index
		"""

		# --- remove the rotamer --- #
		for rot in self.rotamers:
			if rot.index == rotindex:
				self.rotamers.remove(rot)
				break

		# --- remove one-body terms --- #
		for inter in self.nodes:
			if inter.rotindex == rotindex:
				self.nodes.remove(inter)
				break

		# --- remove two-body terms --- #
		cpedges = []
		for inter in self.edges:
			if inter.rotindex1 == rotindex or inter.rotindex2 == rotindex:
				continue

			cpedges.append(inter)
		self.edges = cpedges


	def filter_kind(self, type=0, bInverse=False):
		
		"""
		filters on one type of residue
		"""
		
		edglist = []
		if not bInverse:
			edglist = self.edgesWithType(type)
		else:
			edglist = self.edgesWithoutType(type)

		self.edges = edglist
		self.clean()



	def filter_aatypes(self, type1=0, type2=0, bInv=False):

		"""
		function filter_aatypes: filters based on the types of amino acid-amino acid type
		interactions

		if bInv is false we want ONLY type1-type2 interactions
		if bInv is true we want all NON type1-type2 interactions
		"""

		# --- check one-bodied terms --- #
		type1 = int(type1)
		type2 = int(type2)
		failed = {}
		for inter in self.nodes:
			rot = self.get_rotamer(inter.rotindex)
			if rot.aatype != type1 and rot.aatype != type2:
				if not bInv:
					failed[inter.rotindex] = True

		for key in failed.keys():
			self.removeRotamer(key)

		# --- check two-bodied terms --- #
		cpedge = []
		for inter in self.edges:
			rot1 = self.get_rotamer(inter.rotindex1)
			rot2 = self.get_rotamer(inter.rotindex2)

			if rot1.aatype == type1 and rot2.aatype == type2:
				if not bInv:
					cpedge.append(inter)
				continue

			if rot1.aatype == type2 and rot2.aatype == type1:
				if not bInv:
					cpedge.append(inter)
				continue

			if bInv:
				cpedge.append(inter)

		self.edges = cpedge
		self.clean()



	def filter_neighbors(self, aatype, cutoff, bInverse = False):

		"""
		function filter_neighbors: filters the interaction graph based on the number of 
		neighbors for a given amino acid type

		if bInverse is True, we remove things with number of neighbors < cutoff
		if bInverse is False, we remove things with number of neighbors > cutoff
		"""

		cutoff = float(cutoff)
		aatype = int(aatype)

		failed = {}
		sortkey = self.neighbors.keys()
		sortkey.sort()
		for key in sortkey:
			for rot in self.rotamers:
				if rot.aatype == aatype and rot.seqpos == key:
					if bInverse:
						if self.neighbors[key] < cutoff:
							failed[rot.index] = True 
					else:
						if self.neighbors[key] > cutoff:
							failed[rot.index] = True
			
		for key in failed.keys():
			self.removeRotamer(key)

		self.clean()


	def printStats(self):

		"""
		function printStats: prints the current stats of the interaction graph
		"""
		aatypes = {}
		for rot in self.rotamers:
			if not rot.aatype in aatypes.keys():
				aatypes[rot.aatype] = 0

			aatypes[rot.aatype] += 1

		stat_int = {}
		for edge in self.edges:
			rot1 = edge.type1
			rot2 = edge.type2

			k1 = min(rot1,rot2)
			k2 = max(rot1,rot2)
			key = str(k1) + "_" + str(k2)
			
			if not key in stat_int.keys():
				stat_int[key] = 0

			stat_int[key] += 1
	

			

		print "------------------------------------"
		print "---   Interaction Graph Stats   ---"
		print "-----------------------------------"
		print "number of rotamers:",len(self.rotamers)
		print "number of one-body terms:",len(self.nodes)
		print "number of two-body terms:",len(self.edges)
		print ""
		print "rotamer stats:"
		for key in aatypes.keys():
			print aa3_from_num(key),aatypes[key]

		print "----------------------------------"
		print "interaction stats:"
		for key in stat_int.keys():
			(r1,r2) = key.split("_")	
			k1 = int(r1)
			k2 = int(r2)
			print aa3_from_num(k1),"-",aa3_from_num(k2),stat_int[key]
		print "-----------------------------------"
			


	def filter_resfile(self, resfile=""):

		"""
		function filter_resfile: given a resfile, we filter so that only rotamers of a given
		amino acid type at a given position are kept
		"""

		if resfile == "":
			print "usage: filter_resfile(resfile)"
			return

		# --- read resfile --- #
		try:
			RESFILE = open(resfile)
		except:
			print "unable to open resfile"
			sys.exit()

		lines = RESFILE.readlines()
		nlines = len(lines)
		allowed = {}
		for i in range(26,nlines):
			line = string.rstrip(lines[i])

			cols = line.split()
			if len(cols) == 5:
				seqpos = int(cols[1])
				allowed[seqpos] = {}
				allow  = cols[4]
				for letter in allow:
					na = num_from_aa1(letter)
					allowed[seqpos][na] = True

		RESFILE.close()

		failed = {}
		for rot in self.rotamers:
			if allowed.has_key(rot.seqpos):
				if not allowed[rot.seqpos].has_key(rot.aatype):
					failed[rot.index] = True
			else:
				failed[rot.index] = True

		for key in failed.keys():
			self.removeRotamer(key)
					


	def filter_energy(self, function, value, bOne=True, bTwo=True, type1=0, type2=0):

		"""
		function filter: filters the interaction graph based on energy functions
		"""
		
		failed = {}
		value = float(value)
		# --- check one-bodied --- #
		nfail = 0
		if bOne:
			print "filtering one values"
			for inter in self.nodes:
				bRotType = True
				if type1 != 0 or type2 !=0:
					bRotType = False
					rot = self.get_rotamer(inter.rotindex)
					if rot.aatype == type1 or rot.aatype == type2:
						bRotType = True

				if bRotType:
					if inter.energies[function] > value:
						failed[inter.rotindex] = True
						nfail += 1

		print nfail," 1-body failed"


		for key in failed.keys():
			self.removeRotamer(key)

		# --- now remove two-body terms --- #
		if bTwo:
			cpedge = []
			print "filtering two_bodied values"
			for inter in self.edges:
				bRotType = True
				if type1 != 0 and type2 != 0:
					bRotType = False
					rot1 = self.get_rotamer(inter.rotindex1)
					rot2 = self.get_rotamer(inter.rotindex2)
					
					if rot1.aatype == type1 and rot2.aatype == type2:
						bRotType = True
					if rot1.aatype == type2 and rot2.aatype == type1:
						bRotType = True
								
				if bRotType:
					if inter.energies[function] > value:
						continue

				cpedge.append(inter) # --- should pass

			self.edges = cpedge

		self.clean()



	def clean(self):

		"""
		function clean: cleans the interaction graph.  Useful for removing unused rotamers or
		energy interactions
		"""

		# --- get rid of rotamers not in the two-body terms ---- #
		keep = {}
		for inter in self.edges:
			keep[inter.rotindex1] = True
			keep[inter.rotindex2] = True

		cpone = []
		for inter in self.nodes:
			if keep.has_key(inter.rotindex):
				cpone.append(inter)

		self.nodes = cpone

		cprot = []
		for inter in self.rotamers:
			if keep.has_key(inter.index):
				cprot.append(inter)

		self.rotamers = cprot
		
		# --- get rid of neighborlist no longer present
		cpneigh = {}
		for rot in self.rotamers:
			cpneigh[rot.seqpos] = self.neighbors[rot.seqpos]

		self.neighbors = {}
		self.neighbors = cpneigh
			


	def get_rotamer(self, index=0):	

		"""
		function get_rotamer: returns the rotamer of a given index
		"""

		for rot in self.rotamers:
			if rot.index == index:
				return rot

		return None



	def get_rotamer_partners(self, rotindex=0):
		
		"""
		returns a list of rotamers that interact with the rotamer of given index
		"""

		prtnrs = []
		for two_body in self.edges:
			if two_body.rotindex1 == rotindex:
				prtnrs.append(two_body.rotindex2)
			if two_body.rotindex2 == rotindex:
				prtnrs.append(two_body.rotindex1)
	
		return prtnrs


	def sortEnergies(self):

		"""
		sorts the two-body energy terms
		"""

		self.edges.sort()



	def edgesWithRotamer(self,index=0,edgelist=None):
	
		"""
		returns a list of edges that contain a given rotamer
		"""

		if edgelist == None:
			edgelist = self.edges
	
		result = []
		for edge in edgelist:
			if edge.rotindex1 == index or edge.rotindex2 == index:
				result.append(edge)

		return result



	def edgesWithoutRotamer(self,index=0,edgelist=None):
		
		"""
		returns a list of edges that do not contain a given rotamer
		"""

		if edgelist == None:
			edgelist = self.edges

		result = []
		for edge in edgelist:
			if edge.rotindex1 != index and edge.rotindex2 != index:
				result.append(edge)

		return result



	def edgesWithType(self,mytype=0,edgelist=None):
		
		"""
		returns a list of edges with a given type
		"""

		if edgelist == None:
			edgelist = self.edges

		result = []
		for edge in edgelist:
			if edge.type1 == mytype or edge.type2 == mytype:
				result.append(edge)

		return result



	def edgesWithoutType(self, mytype=0,edgelist=None):

		"""
		returns a list of edges that do not have a given type
		"""
	
		if edgelist == None:
			edgelist = self.edges

		result = []
		for edge in edgelist:
			if edge.type1 != mytype and edge.type2 != mytype:
				result.append(edge)

		return result



	def commonInteraction(self,mytype=0,set1=None,set2=None):

		"""
		keeps rotamers that are involved in multiple types of interactions
		"""

		edglist = self.edgesWithType(mytype)
		nedge = len(edglist)
		failed = {}
		work = []
		for i in range(nedge):
			e1 = edglist[i]
			bKeep = False

			if e1.type1 in set1 or e1.type2 in set1:
				work = set2
			elif e1.type1 in set2 or e1.type2 in set2:
				work = set1
			else:
				work = []

			if len(work) > 0:
				for j in range(i+1,nedge):
					e2 = edglist[j]
					if e2.type1 in work or e2.type2 in work:
						bKeep = True

			if not bKeep:
				if e1.type1 == mytype:
					failed[e1.rotindex1] = True
				elif e1.type2 == mytype:
					failed[e1.rotindex2] = True

		

		for index in failed.keys():
			self.removeRotamer(index)	

		self.clean()



	def commonRotamers(self):

		"""
		checks for common rotamers (same chi angle) that occur after combining
		interaction graphs
		"""

		cprots = 0
		clean_map = {}
		print "cleaning up rotamers"
		for i in range(len(self.rotamers)):
			if self.rotamers[i].index == -1:
				continue

			for j in range(i+1,len(self.rotamers)):
				if self.rotamers[j].index == -1:
					continue

				if self.rotamers[j].aatype != self.rotamers[i].aatype:
					continue

				if self.rotamers[j].seqpos != self.rotamers[i].seqpos:
					continue

				if self.rotamers[i].matchesRot(self.rotamers[j]):
					#print "common: ",self.rotamers[j].aatype,self.rotamers[i].index,self.rotamers[j].index,self.rotamers[i].seqpos,self.rotamers[j].seqpos
					clean_map[self.rotamers[j].index] = self.rotamers[i].index
					self.rotamers[j].index = -1

		cprots = []
		for rot in self.rotamers:
			cprots.append(rot)

		self.rotamers = []
		for rot in cprots:
			if rot.index != -1:
				self.rotamers.append(rot)


		# clean up nodes and edges with old rotamer indices
		print "cleaning up nodes"
		cpnodes = []
		for node in self.nodes:
			cpnodes.append(node)

		self.nodes = []
		for node in cpnodes:
			fndnode = False
			for myrot in clean_map.keys():
				if node.rotindex == myrot:
					fndnode = True
					break

			if not fndnode:
				self.nodes.append(node)

		# clean up edges with old rotamer indices
		print "cleaning up edges"
		for edge in self.edges:
			for myrot in clean_map.keys():
				if edge.rotindex1 == myrot:
					edge.rotindex1 = clean_map[myrot]
					break

			for myrot in clean_map.keys():
				if edge.rotindex2 == myrot:
					edge.rotindex2 = clean_map[myrot]
					break
			
			





	def getTriad(self, triad=""):
		
		"""
		trims the interaction graph to contain only a particular triad
		"""

		if len(triad) != 3:
			print "triad must contain 3 residues"
			return

		a1 = num_from_aa1(triad[0])
		a2 = num_from_aa1(triad[1])
		a3 = num_from_aa1(triad[2])

		a2list = self.edgesWithType(a2)
		a1list = self.edgesWithType(a1,a2list)
		a3list = self.edgesWithType(a3,a2list)

		# save list of non-triad edges
		prevEdges = self.edgesWithoutType(a2)

		# find rotamers that are in common lists
		result = []
		for edge in a1list:
			ri = 0
			if edge.type1 == a2:
				ri = edge.rotindex1
			elif edge.type2 == a2:
				ri = edge.rotindex2

			c3list = self.edgesWithRotamer(ri,a3list)
			if len(c3list) > 0:
				result.append(edge)
				for edge3 in c3list:
					result.append(edge3)

		print "cleaning up edges"
		self.edges = []
		for i in range(len(result)):
			edge = result[i]
			if not edge in self.edges:
				self.edges.append(edge)

		for edge in prevEdges:
			self.edges.append(edge)
		print "cleaning"
		self.clean()
					
			

				


class one_body_interaction:

	"""
	one body interaction class useful for storing one-body energy terms
	"""

	def __init__(self):
		self.energies = {}
		self.rotindex = 0
		self.totE = 0


	def set_energy(self, function, value):

		"""
		function set_energy: sets the value for the given energy function
		"""

		self.energies[function] = value	
		self.totE += value



	def total_energy(self):

		"""
		function total_energy: returns the total energy for this rotamer
		"""

		sum = 0
		for key in self.energies.keys():
			sum += self.energies[key]

		return sum




class two_body_interaction:

	"""
	two body interaction storage class
	"""

	def __init__(self):
		self.energies = {}
		self.rotindex1 = 0
		self.rotindex2 = 0
		self.type1     = 0
		self.type2     = 0
		self.totE = 0


	def __cmp__(self,other):

		"""
		compares two-body energy objects by the total energy
		"""

		return cmp(self.total_energy, other.total_energy)

		

	def set_energy(self, function, value):

		"""
		sets the energy value for the given function
		"""

		self.energies[function] = value	
		self.totE += value



	def total_energy(self):

		"""
		function total_energy: calculates the total energy for this interaction
		"""

		sum = 0
		for key in self.energies.keys():
			sum += self.energies[key]

		return sum
