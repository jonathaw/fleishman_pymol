#!/usr/bin/python

import commands, os, sys, string, re, math


def atomtype_from_virtual(virt_name):

	"""
	returns the rosetta atom type that corresponds to a given virtual atom
	"""

	if virt_name == "VOOC":
		return "OOC "
	if virt_name == "VHNE":
		return "Nhis"   # this has the histidine as a base!!!!
	if virt_name == "VHND":
		return "Nhis"
	if virt_name == "VNOC":
		return "NH2O"
	if virt_name == "VOCN":
		return "ONH2"
	if virt_name == "VSOG":
		return "OH  "
	if virt_name == "VYOH":
		return "OH  "
	if virt_name == "VARO":
		return "aroC"

	print "UNRECOGNIZED VIRTUAL ATOM:",virt_name
	return ""


def residues1_from_virtual(virt_name):

	"""
	releases a string of residues	 from virtual atoms
	"""

	return ""
