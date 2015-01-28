import sys
sys.path.append("/Users/sarelf/python_scripts/pymol_scripts/desview/")
sys.path.append("/Users/sarelf/python_scripts/py_scripts")

from wizard_desview import *
import commands

wiz_view = wizard_desview()
cmd.set_wizard(wiz_view)

global design_files
global curr_design_file
design_files = []
curr_design_file = 0

def loadNative(file):
	if file == "":
		print "USAGE: loadNative(file)"

	[base, rest] = file.split(".pdb", 1)
	print "base = ",base

	cmd.load(file)
	wiz_view.setNative(base)


def loadResfile(file):

	if file == "":
		print "USAGE: loadResfile(file)"
	
	wiz_view.loadResfile(file)


def residuesInSelection(selection=""):

	if selection == "":
		print "usage: residuesInSelection(selection)"
		return

	Taken = {}
	mysel = cmd.get_model(selection)
	natom = len(mysel.atom)
	for i in range(natom):
		Taken[mysel.atom[i].resi] = True

	mylist = []
	for i in Taken.keys():
		mylist.append(int(i))

	mylist.sort()
	return mylist


def loadDesignList(file=""):

	global curr_design_file
	global design_files
	try:
		MYFILES = open(file)
	except:
		print "unable to open file"
		return

	design_files = []
	for line in MYFILES.readlines():
		line = string.rstrip(line)
		design_files.append(line)
		
	curr_design_file = 0


def keep():
	
	global curr_design_file
	mycmd = "mv " + design_files[curr_design_file] + " keep/"
	commands.getoutput(mycmd)
	curr_design_file += 1

	if curr_design_file >= len(design_files):
		print "end of list reached"
		return

	cmd.delete("all")
	print "current file:",design_files[curr_design_file]
	wiz_view.viewer.loadDesign(design_files[curr_design_file])


def reject():

	global curr_design_file
	mycmd = "mv " + design_files[curr_design_file] + " reject/"
	commands.getoutput(mycmd)
	curr_design_file += 1

	if curr_design_file >= len(design_files):
		print "end of list reached"
		return

	cmd.delete("all")
	print "current file:",design_files[curr_design_file]
	wiz_view.viewer.loadDesign(design_files[curr_design_file])


cmd.extend('loadNative', loadNative)
cmd.extend('loadResfile', loadResfile)
cmd.extend('keep', keep)
cmd.extend('reject', reject)
cmd.extend('loadDesignList', loadDesignList)

