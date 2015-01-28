#!/usr/bin/python



__author__ = ['Andrew Wollacott (amw215@u.washington.edu)']
__version__ = "Revision 0.1"

import string, re, random


# -------------------------------------------------------
# -------------------------------------------------------
# -------------------------------------------------------

class FragmentLibrary:
	"""

	A FragmentLibrary stores fragments for a given pdbfile

	"""

	def __init__(self):
		self.positions = []
		random.seed()


	def clear(self):
		for pos in self.positions:
			pos.clear()

		self.positions = []


	def renumberPositions(self):
		i = 0
		for fragpos in self.positions:
			i += 1
			fragpos.setPosition(i)


	def read(self, file=""):
		pos = re.compile(" position")

		try:
			FILE = open(file, 'r')
		except:
			print "unable to open file",file
			return

		fragpos = None
		frag = None
		prevline = ""
		for line in FILE.readlines():
			line = string.rstrip(line)

			if line == "":
				prevline = line
				continue

			if pos.match(line):
				fragpos = self.newPosition()
			else:
				if prevline == "":
					frag = fragpos.newFragment()

				frag.addLine(line)

			prevline = line

		FILE.close()
				
				

	def write(self, file=""):
		try:
			FILE = open(file, 'w')
		except:
			print "unable to open file:",file

		for pos in self.positions:
			ipos = pos.position
			nfrags = pos.numFragments()
			FILE.write(' position: %12i neighbors: %12i\n' % (ipos, nfrags))

			n = 0
			for frag in pos.fragments:
				FILE.write("\n")
				n += 1
				for line in frag.fraglines:
					FILE.write('%84s P%3i F%3i\n' % (line,ipos,n))

			FILE.write("\n")



		FILE.close()
		



	def newPosition(self):
		fragpos = FragmentPosition()
		self.addPosition(fragpos)

		return fragpos


	def addPosition(self, fragpos=None):
		if fragpos == None:
			return

		npos = self.numPositions()
		fragpos.position = npos
		self.positions.append(fragpos)


	def numPositions(self):
		return len(self.positions)



	def getPosition(self, index=-1):
		for frag in self.positions:
			if frag.position == index:
				return frag

		return None


# -------------------------------------------------------
# -------------------------------------------------------
# -------------------------------------------------------

class FragmentPosition:
	"""

	A FragmentPosition stores all fragments for a given residue position

	"""

	def __init__(self):
		self.position  = 0
		self.fragments = []


	def clone(self):
		result = FragmentPosition()
		result.position = self.position

		for frag in self.fragments:
			newfrag = frag.clone()
			result.addFragment(newfrag)

		return result


	def clear(self):
		for frag in self.fragments():
			frag.clear()

		self.fragments = []


	def setPosition(self, pos):
		self.position = pos
		for frag in self.fragments:
			frag.setPosition(pos)


	def numFragments(self):
		return len(self.fragments)


	def newFragment(self):
		frag = Fragment()
		self.addFragment(frag)
		return frag


	def addFragment(self, frag=None):
		if frag == None:
			return

		nfrag = self.numFragments() + 1
		frag.setPosition(nfrag)
		self.fragments.append(frag)

	
	def renumberFragments(self):
		i = 0
		for frag in self.fragments:
			i += 1
			frag.position = i

	
	def getFragment(self, index=0):
		for frag in self.fragments:
			if frag.position == index:
				return frag

		return None


	def getRandFragments(self, nfrags=0):
		# ---   gets nfrags random fragments   --- #
		tot_frags = self.numFragments()
		if nfrags <= 0 or nfrags >= tot_frags:
			return None

		done = False
		taken = [False]*tot_frags
		
		result = []
		ntaken = 0
		while not done:
			ind = random.randint(0,tot_frags-1)
			if not taken[ind]:
				result.append(self.fragments[ind])
				taken[ind] = True
				ntaken += 1

				if ntaken == nfrags:
					done = True

		return result


				





# -------------------------------------------------------
# -------------------------------------------------------
# -------------------------------------------------------

class Fragment:
	"""

	A Fragment contains the information related to a fragment

	"""

	def __init__(self):
		self.fraglines = []
		self.position  = 0


	def clone(self):
		result = Fragment()
		result.position = self.position

		for fragline in self.fraglines:
			result.addLine(fragline)

		return result


	def clear(self):
		self.fraglines = []
		self.position = 0


	def setPosition(self, pos):
		self.position = pos
		

	def addLine(self, line=""):
		info = line[1:84]
		self.fraglines.append(info)
		


