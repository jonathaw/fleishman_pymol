#!/usr/bin/python

from Molecule import *
import commands, os, sys, string, re



def HBenergy(D=None, H=None, A=None, AA=None, donor=None, acceptor=None):

	if donor != None:
		D = donor.D
		H = donor.H

	if acceptor != None:
		A  = acceptor.A
		AA = acceptor.AA

	dist = H.distance(A)
	HBE = 0.0
	if dist < 2.0:
		ang1 = vector3d.angle3(H,A,AA)
		if ang1 > 120.0:
			ang2 = vector3d.angle3(D,H,A)
			ang2 = math.radians(ang2)
			cos2 = math.cos(ang2)
			HBE = -1.0*(cos2*cos2)*math.exp(-1.0*dist*dist)

	return HBE

