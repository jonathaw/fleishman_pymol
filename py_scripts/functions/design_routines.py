#!/usr/bin/python

import string

def getSubstitutionPositions(native_sequence="", design_sequence=""):

	"""
	returns a list of positions that have been substituted
	"""

	subs = []
	mysize = len(native_sequence)
	if len(native_sequence) != len(design_sequence):
		print "lengths differ"
		mysize = min(len(native_sequence),len(design_sequence))

	for i in range(mysize):
		if native_sequence[i] != design_sequence[i]:
			subs.append(i+1)

	return subs



def numSubstitutions(native_sequence="", design_sequence=""):

	"""
	returns the number of substitions
	"""

	if len(native_sequence) != len(design_sequence):
		return 0

	nsubs = 0
	for i in range(len(native_sequence)):
		if native_sequence[i] != design_sequence[i]:
			nsubs += 1

	return nsubs

